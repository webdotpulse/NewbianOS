"""
Multimodal Voice Macro Engine & Voice-Driven Terminal Gestures
Maps natural developer voice shortcuts to complex shell, Git, container, and swarm actions.
"""

import asyncio
import logging
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger("jarvis.macros")

@dataclass
class VoiceMacro:
    macro_id: str
    patterns: List[str]
    description: str
    command_template: str
    category: str  # "git", "docker", "swarm", "system", "containers"

class VoiceMacroEngine:
    def __init__(self):
        self.macros: List[VoiceMacro] = []
        self._register_default_macros()

    def _register_default_macros(self):
        """Register built-in voice macros."""
        # 1. Git Workflow Macros
        self.macros.append(VoiceMacro(
            macro_id="git_rebase_push",
            patterns=[
                r".*rebase on main and force push.*",
                r".*rebase main force push.*",
                r".*rebase and push.*"
            ],
            description="Rebase current branch on origin/main and force push safely",
            command_template="git pull --rebase origin main && git push --force-with-lease",
            category="git"
        ))
        self.macros.append(VoiceMacro(
            macro_id="git_status_diff",
            patterns=[
                r".*show git status.*",
                r".*what changed in git.*",
                r".*git diff summary.*"
            ],
            description="Display git status and diff statistics",
            command_template="git status --short && git diff --stat",
            category="git"
        ))

        # 2. Terminal & Container Gestures
        self.macros.append(VoiceMacro(
            macro_id="terminal_split_logs",
            patterns=[
                r".*split terminal and tail docker logs.*",
                r".*split terminal tail logs.*",
                r".*tail container logs.*"
            ],
            description="Split terminal and tail active container logs",
            command_template="tmux split-window -h 'docker logs -f $(docker ps -q -l)'",
            category="docker"
        ))
        self.macros.append(VoiceMacro(
            macro_id="launch_agy_box",
            patterns=[
                r".*launch agy box.*",
                r".*spawn devcontainer.*",
                r".*start project container.*"
            ],
            description="Launch ephemeral micro-container environment",
            command_template="agy-box up",
            category="containers"
        ))

        # 3. Antigravity Swarm Gestures
        self.macros.append(VoiceMacro(
            macro_id="swarm_security_audit",
            patterns=[
                r".*swarm audit code.*",
                r".*run security swarm.*",
                r".*audit security vulnerabilities.*"
            ],
            description="Trigger autonomous security swarm agent audit",
            command_template="agy-swarm spawn security 'Automated voice-triggered security scan'",
            category="swarm"
        ))
        self.macros.append(VoiceMacro(
            macro_id="swarm_test_fixer",
            patterns=[
                r".*swarm fix tests.*",
                r".*run test swarm.*",
                r".*fix all broken tests.*"
            ],
            description="Trigger autonomous test runner & auto-fix agent",
            command_template="agy-swarm spawn test 'Diagnose and run all unit tests'",
            category="swarm"
        ))

        # 4. Instant Rollback & Snapshot Gestures
        self.macros.append(VoiceMacro(
            macro_id="atomic_snapshot_now",
            patterns=[
                r".*take system snapshot.*",
                r".*create rollback point.*",
                r".*save restore point.*"
            ],
            description="Create instant Btrfs rollback snapshot",
            command_template="newbian-rollback create 'Voice-triggered restore checkpoint'",
            category="system"
        ))

    def match_macro(self, speech_text: str) -> Optional[Tuple[VoiceMacro, str]]:
        """
        Evaluate if user speech matches any registered voice macro.
        Returns (matched_macro, executable_command) or None.
        """
        cleaned = speech_text.lower().strip()
        # Strip common wake prefixes
        cleaned = re.sub(r'^(hey\s+)?jarvis[,\s]*', '', cleaned).strip()

        for macro in self.macros:
            for pattern in macro.patterns:
                if re.match(pattern, cleaned):
                    logger.info(f"Matched Voice Macro: [{macro.macro_id}] -> {macro.command_template}")
                    return (macro, macro.command_template)

        return None
