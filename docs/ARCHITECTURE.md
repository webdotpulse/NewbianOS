# NewbianOS Operating System Architecture

## 1. Upstream Foundation & Hardware Acceleration
- **Base Distribution**: Debian 13 ("Trixie") amd64.
- **Kernel**: Linux Kernel 7.x and upwards (`linux-image-amd64` v7+ standard) with `PREEMPT_DYNAMIC` low-latency scheduling, Btrfs subvolumes, eBPF telemetry, and non-free OEM firmware (`firmware-linux-nonfree`, `intel-microcode`, `amd64-microcode`).
- **NPU Acceleration HAL**: Dedicated Neural Processing Unit layer (`Intel OpenVINO/IVPU`, `AMD Ryzen AI XDNA`, `NVIDIA TensorRT-LLM`, `Qualcomm Hexagon`) providing 48+ TOPS low-power neural inference for local voice, vision, and reasoning models.
- **Desktop Environment**: KDE Plasma 6 with native Wayland session (`plasma-workspace-wayland`, `kwin-wayland`).
- **Audio & Spatial Video**: PipeWire 3D spatial audio server with binaural HRTF positioning, WirePlumber session manager, V4L2 loopback kernel module.
- **Init System**: Systemd with user session targets and `systemd-sysext` mutable extension layers.

## 2. Package Management & Repositories
NewbianOS includes pre-configured APT repositories with verified GPG keychains:
- `main contrib non-free non-free-firmware` (Debian 13 Trixie + Backports)
- Official Google Chrome Stable (`https://dl.google.com/linux/chrome/deb/`)
- Official Docker CE (`https://download.docker.com/linux/debian`)
- NodeSource Node.js 22 LTS (`https://deb.nodesource.com/node_22.x`)
- Flatpak & Flathub integration

## 3. Storage, Atomic Core & Instant Rollbacks
- **Root Filesystem**: Btrfs with atomic subvolumes:
  - `@` -> `/` (Immutable / Transactional Root)
  - `@home` -> `/home` (Developer Workspace)
  - `@var` -> `/var` (Dynamic Logs, Flatpaks & Containers)
  - `@snapshots` -> `/.snapshots` (Snapper Rollback Archive)
  - `@opt` -> `/opt` (Third-Party SDKs & IDEs)
- **Instant Rollback**: 2-second GRUB bootloader snapshot recovery and CLI management via `newbian-rollback`.
- **Compression**: Transparent `zstd:1` compression enabled by default.
- **Cloud Workspace**: Native FUSE filesystem mounted at `~/GoogleDrive`.
- **Ephemeral Containers**: Isolated project sandboxes via `agy-box` (`agy up`) with Wayland GUI forwarding, GPU pass-through, and `*.dev.local` local DNS resolution.

## 4. Multi-Agent AI & Swarm Orchestration
- **Local Semantic Code Graph**: In-memory AST and vector chunk indexer scanning local Git repositories for sub-millisecond context retrieval (`agy index`, `agy search`).
- **Antigravity Swarm Orchestrator**: Background worker agents for security audits, test runner diagnosis, refactoring analysis, and pull request synthesis (`agy swarm`).
- **IPC Event Bus**: Standardized D-Bus and UNIX socket event bus (`org.newbianos.AgentEvents`) synchronizing notifications with KDE Plasma widgets, the SDDM lockscreen, and the Holographic HUD.

## 5. Cloud Workstation Streaming & Spatial WebXR HUD
- **Wayland Direct Scanout Streamer**: 4K 120fps AV1/HEVC hardware encoding with WebRTC low-latency streaming to remote thin clients, iPads, MacBooks, and VR/AR headsets (`newbian-stream`).
- **Spatial Holographic HUD**: True 3D WebXR/OpenXR spatial canvas with floating terminal windows, AI Swarm monitors, and 6-DoF head-tracking matrix integration.

## 6. Zero-Trust Hardware Enclave & Biometrics
- **Jarvis PAM Biometric Module**: Optical face tracking PAM helper (`pam_jarvis_face.so`) for instant SDDM login and passwordless `sudo` execution when the authorized developer is present.
- **TPM2 Full-Disk Encryption**: Automated LUKS2 disk key unsealing bound to PCR0+PCR7 Secure Boot states via `systemd-cryptenroll`.
- **Hardware FIDO2 Security**: Seamless WebAuthn hardware key integration for SSH and Git commit signing (`git-fido-sign` / `ssh-ed25519-sk`).
