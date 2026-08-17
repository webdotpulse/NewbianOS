# NewbianOS Operating System Architecture

## 1. Upstream Foundation
- **Base Distribution**: Debian 13 ("Trixie") amd64.
- **Kernel**: Linux Kernel 7.x and upwards (`linux-image-7-amd64` / `linux-image-amd64` v7+ standard) with `PREEMPT_DYNAMIC` low-latency scheduling, bcachefs support, eBPF telemetry, and standard non-free firmware packages (`firmware-linux-nonfree`, `firmware-misc-nonfree`, `intel-microcode`, `amd64-microcode`).
- **Desktop Environment**: KDE Plasma 6 with native Wayland session (`plasma-workspace-wayland`, `kwin-wayland`).
- **Audio & Video Subsystem**: PipeWire audio server, WirePlumber session manager, V4L2 loopback kernel module.
- **Init System**: Systemd with user session targets.

## 2. Package Management & Repositories
NewbianOS includes pre-configured APT repositories with verified GPG keychains:
- `main contrib non-free non-free-firmware` (Debian 13 Trixie + Backports)
- Official Google Chrome Stable (`https://dl.google.com/linux/chrome/deb/`)
- Official Docker CE (`https://download.docker.com/linux/debian`)
- NodeSource Node.js 22 LTS (`https://deb.nodesource.com/node_22.x`)
- Flatpak & Flathub integration

## 3. Storage & Filesystem Strategy
- **Root Filesystem**: Btrfs with `@` (root) and `@home` (user data) subvolumes.
- **Compression**: Transparent `zstd:1` compression enabled by default.
- **Cloud Workspace**: Native FUSE filesystem mounted at `~/GoogleDrive`.
- **Swap**: Dynamic zram swap device for high-performance memory paging.

## 4. Security & Permissions Architecture
- **Polkit**: Custom action policies located in `/usr/share/polkit-1/actions/` granting Jarvis controlled OS execution authority.
- **Keyring**: SecretService / KWallet backend for Google Drive OAuth2 token storage.
- **Ozone Platform Isolation**: Electron and Chromium apps execute with Wayland Ozone hardware acceleration.
