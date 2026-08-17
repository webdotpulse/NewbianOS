# NewbianOS Developer Guide

## 1. Antigravity-IDE & AI Pair Programming
Antigravity-IDE is the default IDE in NewbianOS.

### Launching:
- Graphical shortcut: `Super + A`
- Command Line: `antigravity-ide .` or `agy chat`

### Pre-Configured Toolchains:
- **Node.js**: v22 LTS pre-installed with `npm`, `npx`, and `corepack` (pnpm / yarn).
- **Python**: Python 3.13 with `uv`, `poetry`, `pipx`, and virtualenv.
- **Containers**: Docker CE & Podman pre-configured with rootless permissions.
- **Git**: Configured with `delta` diff pager, syntax highlighting, and Starship branch badges.

---

## 2. Google Drive Workspace Sync (`~/GoogleDrive`)
All files saved in `~/GoogleDrive` are automatically synced to Google Cloud Workspace in the background.

- Check status: `gdrive status`
- Force sync: `gdrive sync`
- Dolphin Integration: Right-click any file in Dolphin to copy the Google Drive share link or sync instantly.

---

## 3. Figma Desktop & Local Font Helper
NewbianOS includes a local font daemon running on `127.0.0.1:18412` (`figma-font-helper`).
When using Figma in the browser or via `figma-desktop`, all installed developer fonts (JetBrains Mono, Inter, Fira Code, Roboto, Geist) are accessible on your canvas immediately without manual font uploads.
