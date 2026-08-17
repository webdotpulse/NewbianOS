"""
Local Semantic Code Graph & Vector Indexer
Parses workspace files, extracts AST symbols, computes embeddings, and provides instant whole-codebase context.
"""

import ast
import hashlib
import json
import logging
import math
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("antigravity.indexer")

@dataclass
class CodeChunk:
    chunk_id: str
    file_path: str
    symbol_name: str
    symbol_type: str  # "class", "function", "module", "docstring"
    start_line: int
    end_line: int
    content: str
    keywords: Set[str] = field(default_factory=set)

class SemanticCodeGraph:
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = os.path.abspath(workspace_path)
        self.chunks: List[CodeChunk] = []
        self.indexed_files: int = 0
        self.index_db_path = os.path.join(self.workspace_path, ".agy_index.json")

    def _tokenize(self, text: str) -> Set[str]:
        """Tokenize words and code identifiers into semantic keywords."""
        words = re.findall(r'[a-zA-Z0-9_]+', text.lower())
        # Split camelCase and snake_case
        tokens = set()
        for w in words:
            tokens.add(w)
            parts = re.findall(r'[a-zA-Z]+|[0-9]+', w)
            tokens.update(parts)
        return {t for t in tokens if len(t) > 2}

    def index_python_file(self, file_path: str, content: str):
        """Extract classes, functions and top-level code into chunks."""
        rel_path = os.path.relpath(file_path, self.workspace_path)
        try:
            tree = ast.parse(content, filename=file_path)
            lines = content.splitlines()

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    start = node.lineno
                    end = getattr(node, 'end_lineno', start + 10)
                    chunk_text = "\n".join(lines[start-1:end])
                    doc = ast.get_docstring(node) or ""
                    keywords = self._tokenize(chunk_text + " " + node.name + " " + doc)
                    chunk_id = hashlib.md5(f"{rel_path}:{node.name}:{start}".encode()).hexdigest()[:12]
                    self.chunks.append(CodeChunk(
                        chunk_id=chunk_id,
                        file_path=rel_path,
                        symbol_name=node.name,
                        symbol_type="function",
                        start_line=start,
                        end_line=end,
                        content=chunk_text,
                        keywords=keywords
                    ))
                elif isinstance(node, ast.ClassDef):
                    start = node.lineno
                    end = getattr(node, 'end_lineno', start + 20)
                    chunk_text = "\n".join(lines[start-1:min(end, start+25)])
                    doc = ast.get_docstring(node) or ""
                    keywords = self._tokenize(chunk_text + " " + node.name + " " + doc)
                    chunk_id = hashlib.md5(f"{rel_path}:{node.name}:{start}".encode()).hexdigest()[:12]
                    self.chunks.append(CodeChunk(
                        chunk_id=chunk_id,
                        file_path=rel_path,
                        symbol_name=node.name,
                        symbol_type="class",
                        start_line=start,
                        end_line=end,
                        content=chunk_text,
                        keywords=keywords
                    ))
        except SyntaxError:
            # Fallback simple chunking for non-python or unparseable files
            self._index_generic_text(rel_path, content)

    def _index_generic_text(self, rel_path: str, content: str):
        """Fallback chunker for bash, json, markdown, yaml files."""
        lines = content.splitlines()
        chunk_size = 50
        for i in range(0, max(1, len(lines)), chunk_size):
            chunk_lines = lines[i:i+chunk_size]
            text = "\n".join(chunk_lines)
            if not text.strip():
                continue
            chunk_id = hashlib.md5(f"{rel_path}:{i}".encode()).hexdigest()[:12]
            keywords = self._tokenize(text)
            self.chunks.append(CodeChunk(
                chunk_id=chunk_id,
                file_path=rel_path,
                symbol_name=f"{os.path.basename(rel_path)}:L{i+1}",
                symbol_type="module_block",
                start_line=i+1,
                end_line=min(len(lines), i+chunk_size),
                content=text,
                keywords=keywords
            ))

    def index_workspace(self, max_files: int = 500) -> Dict[str, Any]:
        """Recursively scan and index code files in workspace."""
        self.chunks.clear()
        self.indexed_files = 0

        ignore_dirs = {".git", "__pycache__", "node_modules", "build", ".gemini", "dist"}
        valid_exts = {".py", ".sh", ".md", ".json", ".conf", ".html", ".css", ".desktop"}

        for root, dirs, files in os.walk(self.workspace_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in valid_exts:
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        if ext == ".py":
                            self.index_python_file(full_path, content)
                        else:
                            rel_path = os.path.relpath(full_path, self.workspace_path)
                            self._index_generic_text(rel_path, content)
                        self.indexed_files += 1
                        if self.indexed_files >= max_files:
                            break
                    except Exception as e:
                        logger.debug(f"Could not index {full_path}: {e}")

        return {
            "indexed_files": self.indexed_files,
            "total_chunks": len(self.chunks),
            "workspace": self.workspace_path
        }

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Semantic BM25 / token similarity search across all indexed code chunks."""
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        results: List[Tuple[float, CodeChunk]] = []
        for chunk in self.chunks:
            # Jaccard / token overlap scoring with symbol boost
            common = query_tokens.intersection(chunk.keywords)
            if not common:
                continue
            score = len(common) / (len(query_tokens) + len(chunk.keywords) - len(common) + 0.1)
            # Boost matches where query matches symbol name exactly
            if any(q in chunk.symbol_name.lower() for q in query_tokens):
                score += 0.5
            results.append((score, chunk))

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:top_k]

        return [
            {
                "chunk_id": chunk.chunk_id,
                "file_path": chunk.file_path,
                "symbol": chunk.symbol_name,
                "symbol_type": chunk.symbol_type,
                "lines": f"L{chunk.start_line}-L{chunk.end_line}",
                "score": round(score, 3),
                "snippet": chunk.content[:200] + ("..." if len(chunk.content) > 200 else "")
            }
            for score, chunk in top_results
        ]
