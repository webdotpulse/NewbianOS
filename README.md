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
- **NPU Neural Hardware Acceleration**: Sub-10ms inference supporting Intel OpenVINO, AMD Ryzen AI XDNA, and NVIDIA TensorRT-LLM with GGUF/ONNX quantized models (48+ TOPS at 2.4W).
- **PipeWire 3D Spatial Audio & Voice Macros**: 3D binaural HRTF sound positioning matching active Wayland window coordinates, plus developer voice shortcuts (*"rebase on main and force push"*, *"split terminal and tail logs"*).
- **Optical Vision & Face Biometrics**: V4L2 camera user perception with real-time face tracking, eye gaze direction, and zero-trust PAM face unlock (`pam_jarvis_face`).
- **Screen Perception**: Wayland PipeWire screencast OCR and window context sensor for real-time IDE and terminal awareness.
- **Deep OS Execution Authority**: Polkit-authorized system execution across hardware telemetry (CPU, GPU, NPU, RAM, thermals), container management, package installations, systemd services, and instant Btrfs snapshots.
- **Spatial Holographic HUD (`jarvis-hud`)**: Cyberpunk glassmorphic overlay with WebXR 3D spatial mode, animated Arc-Reactor core, audio-reactive waveform visualizer, and live swarm monitors.

### 3. 🔄 Immutable Atomic Core & Instant Btrfs Rollbacks (`newbian-rollback`)
- **Transactional Base System**: Atomic Btrfs subvolumes (`@`, `@home`, `@var`, `@snapshots`, `@opt`) and `systemd-sysext` mutable extension layers.
- **2-Second Rollback**: Instant boot recovery via Snapper and GRUB snapshot menus.

### 4. 🐝 Antigravity Multi-Agent Swarm (`agy swarm` / `agy-swarm`)
- **Local Semantic Code Graph**: Vector AST indexing across local repositories for instant semantic code search and context retrieval.
- **Autonomous Worker Swarms**: Background AI agents for security audits, test runner diagnosis, refactoring, and automated PR preparation over D-Bus (`org.newbianos.AgentEvents`).

### 5. 📦 Ephemeral Micro-Containers (`agy-box` / `agy up`)
- **Disposable Dev Environments**: Instant container provisioning from `.devcontainer.json` or Dockerfiles with GPU pass-through, Wayland GUI forwarding, and `~/GoogleDrive` mounting.
- **Zero-Config Networking**: Automatic `*.dev.local` local DNS routing with SSL termination.

### 6. 🌐 Cloud Workstation Streaming & WebXR Spatial HUD (`newbian-stream`)
- **Direct Wayland Scanout**: Hardware-accelerated 4K 120fps AV1/HEVC WebRTC streaming to iPads, MacBooks, and VR/AR spatial headsets (Apple Vision Pro, Meta Quest).

### 7. 🛡️ Zero-Trust Hardware Enclave (`newbian-tpm-enclave`)
- **TPM2 & Secure Boot**: Automatic LUKS2 key unsealing bound to PCR0+PCR7 states via `systemd-cryptenroll`.
- **FIDO2 / WebAuthn Hardware Keys**: Frictionless developer Git commit signing and SSH key auth.

### 8. 🌐 Official Google Chrome Integration
- **Widevine DRM & Chrome Sync**: Pre-configured with official Google Linux repository.
- **Hardware Video Acceleration**: Full VA-API and Vulkan hardware acceleration on Intel, AMD, and NVIDIA graphics.

### 9. ☁️ Native Google Drive Workspace (`~/GoogleDrive`)
- **Direct Filesystem Mount**: Bidirectional FUSE & Inotify sync engine seamlessly mounted at `~/GoogleDrive`.
- **KDE Dolphin Integration**: Pinned Google Drive bookmark in Dolphin Places sidebar with context actions (*"Sync Now"*, *"Share Link"*).

### 10. 🎨 Figma Desktop & Local Font Helper
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
# Antigravity CLI & Swarm
agy chat
agy swarm spawn security "Audit all privileged calls"
agy up                  # Launch ephemeral project container (.devcontainer.json)
agy index .             # Build local semantic code graph

# Jarvis Multimodal AI & Voice Macros
jarvis "rebase on main and force push"
jarvis "Deploy docker containers and report status"
jarvis --look           # Inspect active screen and error context
jarvis --status         # Display hardware, NPU and face perception vitals
jarvis --hud            # Open the Holographic HUD overlay

# Instant Btrfs Rollback & Snapshots
newbian-rollback list
newbian-rollback rollback 1

# Cloud Workstation Streaming
newbian-stream start 4k120
newbian-stream status

# Zero-Trust TPM2 & FIDO2 Enclave
newbian-tpm-enclave status
newbian-tpm-enclave fido-sign

# Google Drive Cloud Sync
gdrive status           # Check sync status and storage quota
gdrive sync             # Trigger immediate bidirectional sync
gdrive auth             # Connect Google Cloud account
```

---

## 💾 Download & USB Installation

1. **Download Pre-Built ISO**: Grab the latest release ISO (`NewbianOS-13-Nexus-*.iso`) and cryptographic SHA-256 checksums from [GitHub Releases](https://github.com/webdotpulse/NewbianOS/releases). Every tagged release automatically triggers a fresh ISO build via GitHub Actions.
2. **Create Bootable USB**: Follow our step-by-step flashing guide for Windows, Linux, and macOS:
   👉 **[Full Guide: Creating an Installable USB Drive](file:///home/koen/git/NewbianOS/docs/CREATE_USB_INSTALLER.md)**

---

## 🛠️ Building the Bootable Live ISO Locally

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
