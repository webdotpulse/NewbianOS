# NewbianOS 13 "Nexus" — AI-Native Developer Operating System

```
   ___          __  _                         _  __           
  / _ | ___  __/ /_(_)__ ________ __  _____ _(_) /___ __ _____
 / __ |/ _ \/ _  / / _  / __/ _  /\ \/ / _  / / __/ // // _ \
/_/ |_/_//_/\_,_/_/\_, /_/  \_,_/  \_/ \_,_/_/\__/\_, // .__/
                  /___/                           /__//_/    
  ⚡ Modern, AI-Native Linux Distribution derived from Debian & KDE Plasma 6
```

**NewbianOS** is a next-generation, developer-ready Linux distribution built on **Debian 13 (Trixie)**, **Linux Kernel 7.x+ (PREEMPT_DYNAMIC standard)**, and **KDE Plasma 6 (Wayland Native)**. It provides an out-of-the-box, AI-first computing environment pre-configured with **Antigravity-IDE**, **Jarvis Multimodal Voice & Vision Assistant**, **Official Google Chrome**, **Native Google Drive Workspace Sync**, and **Figma Desktop**.

---

## 🌟 Key Out-of-the-Box Features

### 1. 🤖 Antigravity-IDE Out-of-the-Box
- **AI-Native Development Environment**: Pre-installed and hardware-accelerated with Wayland Ozone, WebRTC PipeWire screen capturer, and GPU rasterization.
- **Universal Developer Toolchain**: Node.js 22 LTS, Python 3.13 (with `uv`, `poetry`, `pipx`), Rust, Go, Git (with Delta diff pager), Docker CE, Podman, and Neovim.
- **Antigravity CLI (`agy` / `antigravity`)**: Instant terminal companion for AI agent orchestration, planning mode, and automated test fixes.

### 2. ⚡ Jarvis Multimodal AI Voice & Vision Assistant
- **On-Device Voice Engine**: PipeWire low-latency audio capture, Voice Activity Detection (VAD), Wake-word listener (*"Hey Jarvis"*), and Neural TTS speech synthesis.
- **Optical Vision & Face Tracking**: V4L2 camera user perception with real-time face tracking, eye gaze direction, and user proximity detection.
- **Screen Perception**: Wayland PipeWire screencast OCR and window context sensor for real-time IDE and terminal awareness.
- **Deep OS Execution Authority**: Polkit-authorized system execution across hardware telemetry (CPU, GPU, RAM, temps), container management (`docker compose`), package installations (`apt`, `flatpak`), systemd services, and audio/display controls.
- **Holographic Sci-Fi HUD (`jarvis-hud`)**: Glassmorphic overlay with animated Arc-Reactor core, audio-reactive waveform visualizer, face-tracking reticle, and system diagnostic monitors.

### 3. 🌐 Official Google Chrome Integration
- **Widevine DRM & Chrome Sync**: Pre-configured with official Google Linux repository.
- **Hardware Video Acceleration**: Full VA-API and Vulkan hardware acceleration on Intel, AMD, and NVIDIA graphics.

### 4. ☁️ Native Google Drive Workspace (`~/GoogleDrive`)
- **Direct Filesystem Mount**: Bidirectional FUSE & Inotify sync engine seamlessly mounted at `~/GoogleDrive`.
- **KDE Dolphin Integration**: Pinned Google Drive bookmark in Dolphin Places sidebar with context actions (*"Sync Now"*, *"Share Link"*).

### 5. 🎨 Figma Desktop & Local Font Helper
- **GPU-Accelerated Design**: Figma desktop workspace with Ozone Wayland flags.
- **Local Font Daemon (`figma-font-helper`)**: Runs on `127.0.0.1:18412` exposing all installed local developer fonts (JetBrains Mono, Inter, Fira Code, Geist Mono) directly inside Figma.

---

## 🚀 Quick Start & Commands

### Global Desktop Shortcuts
| Shortcut | Action |
|---|---|
| `Super + Space` | Toggle Jarvis Holographic HUD Overlay |
| `Super + A` | Launch Antigravity-IDE |
| `Super + T` | Open Developer Terminal (Konsole with Zsh + Starship) |
| `Super + E` | Open Dolphin File Manager (with `~/GoogleDrive`) |
| `Super + C` | Open Google Chrome (Hardware-Accelerated) |
| `Super + F` | Launch Figma Desktop |

### CLI Commands
```bash
# Antigravity CLI
agy chat
agy "Fix failing unit tests in ./src"

# Jarvis Multimodal AI
jarvis "Deploy docker containers and report status"
jarvis --look           # Inspect active screen and error context
jarvis --status         # Display hardware vitals and face perception
jarvis --hud            # Open the Holographic HUD overlay

# Google Drive Cloud Sync
gdrive status           # Check sync status and storage quota
gdrive sync             # Trigger immediate bidirectional sync
gdrive auth             # Connect Google Cloud account
```

---

## 🛠️ Building the Bootable Live ISO

```bash
# 1. Install build dependencies on Debian/Ubuntu
sudo ./scripts/install-host-deps.sh

# 2. Run automated verification test suite
make test

# 3. Build hybrid bootable Live ISO
make iso

# 4. Test the generated ISO in QEMU/KVM virtual machine
make test-vm
```

---

## 📂 Repository Structure

```
NewbianOS/
├── Makefile                       # Build, test, and VM targets
├── iso-builder/                   # Debian Live-Build configuration
│   ├── auto/config               # Live-build recipe (Debian 13 Trixie + KDE)
│   ├── config/package-lists/     # Package lists (KDE, Dev stack, Drivers)
│   ├── config/archives/          # Chrome, Docker, NodeSource APT repositories
│   └── config/hooks/normal/      # Chroot configuration hooks
├── installer/                     # Calamares modern installer
│   ├── calamares/settings.conf   # Installer pipeline
│   └── calamares/branding/       # NewbianOS branding & QML slideshow
├── packages/                      # Core OS Packages & Integrations
│   ├── antigravity-integration/  # Antigravity-IDE launcher & agy CLI
│   ├── jarvis-assistant/         # Jarvis multimodal daemon, HUD & CLI
│   ├── google-chrome-integration/# Chrome Wayland & VA-API integration
│   ├── google-drive-sync/        # FUSE sync daemon & Dolphin KIO actions
│   └── figma-integration/        # Figma launcher & local font helper
├── theme/                         # KDE Plasma 6 NeoDark theme & presets
│   └── skel/                     # Starship prompt, Zshrc, KWin shortcuts
├── scripts/                       # ISO builder and QEMU test scripts
├── tests/                         # Unit & integration test suites
└── docs/                          # Comprehensive technical documentation
```

---

## 📜 License
NewbianOS is distributed under the GNU General Public License v3.0 (GPLv3).
