#!/usr/bin/env bash
# ==============================================================================
# NewbianOS Live ISO Builder Orchestration Script
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$ROOT_DIR/build/iso"
ISO_CONFIG_DIR="$ROOT_DIR/iso-builder"

echo "======================================================================"
echo "⚡ NewbianOS 13 'Nexus' Live ISO Generator"
echo "======================================================================"

# Check root/sudo permissions
if [[ $EUID -ne 0 ]]; then
   echo "❌ Error: This script must be run as root (sudo ./scripts/build-iso.sh)" 
   exit 1
fi

# Check required host utilities
REQUIRED_TOOLS=("debootstrap" "xorriso" "grub-mkrescue" "isohybrid")
MISSING_TOOLS=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &>/dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [[ ${#MISSING_TOOLS[@]} -gt 0 ]]; then
    echo "⚠️  Missing build tools: ${MISSING_TOOLS[*]}"
    echo "   Installing build dependencies via apt..."
    apt-get update && apt-get install -y debootstrap debian-archive-keyring xorriso isolinux syslinux-efi syslinux-utils grub-efi-amd64-bin grub-pc-bin grub-common dosfstools mtools squashfs-tools git make ca-certificates gettext po4a
fi

# Ensure modern Debian live-build is installed
if ! command -v lb &>/dev/null || ! lb config --help 2>&1 | grep -q "iso-hybrid"; then
    echo "📦 Installing official modern live-build from salsa.debian.org..."
    TEMP_LB_DIR=$(mktemp -d)
    git clone --depth=1 https://salsa.debian.org/live-team/live-build.git "$TEMP_LB_DIR"
    (cd "$TEMP_LB_DIR" && make install)
    rm -rf "$TEMP_LB_DIR"
fi

# Clean and prepare workspace
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

echo "📦 Syncing live-build configuration tree..."
mkdir -p auto config
cp -r "$ISO_CONFIG_DIR/auto/"* auto/ 2>/dev/null || true
cp -r "$ISO_CONFIG_DIR/config/"* config/ 2>/dev/null || true

# Overlay packages and applications into includes.chroot
echo "📦 Injecting NewbianOS custom packages and daemons into chroot overlay..."
INCLUDES_ROOT="$BUILD_DIR/config/includes.chroot"
mkdir -p "$INCLUDES_ROOT/usr/bin"
mkdir -p "$INCLUDES_ROOT/usr/lib/newbian"
mkdir -p "$INCLUDES_ROOT/usr/share/applications"
mkdir -p "$INCLUDES_ROOT/usr/share/polkit-1/actions"
mkdir -p "$INCLUDES_ROOT/usr/lib/systemd/user"
mkdir -p "$INCLUDES_ROOT/etc/skel/.config"
mkdir -p "$INCLUDES_ROOT/etc/skel/.gemini/antigravity-cli"
mkdir -p "$INCLUDES_ROOT/etc/skel/.local/share"

# Copy Antigravity integration
cp "$ROOT_DIR/packages/antigravity-integration/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/packages/antigravity-integration/share/applications/"* "$INCLUDES_ROOT/usr/share/applications/" 2>/dev/null || true
cp -r "$ROOT_DIR/packages/antigravity-integration/skel/." "$INCLUDES_ROOT/etc/skel/" 2>/dev/null || true

# Copy Jarvis assistant
mkdir -p "$INCLUDES_ROOT/usr/lib/newbian/jarvis"
cp -r "$ROOT_DIR/packages/jarvis-assistant/jarvis/"* "$INCLUDES_ROOT/usr/lib/newbian/jarvis/" 2>/dev/null || true
cp "$ROOT_DIR/packages/jarvis-assistant/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/packages/jarvis-assistant/share/applications/"* "$INCLUDES_ROOT/usr/share/applications/" 2>/dev/null || true
cp "$ROOT_DIR/packages/jarvis-assistant/systemd/"* "$INCLUDES_ROOT/usr/lib/systemd/user/" 2>/dev/null || true
cp "$ROOT_DIR/packages/jarvis-assistant/polkit/"* "$INCLUDES_ROOT/usr/share/polkit-1/actions/" 2>/dev/null || true

# Copy Google Chrome integration
cp "$ROOT_DIR/packages/google-chrome-integration/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/packages/google-chrome-integration/share/applications/"* "$INCLUDES_ROOT/usr/share/applications/" 2>/dev/null || true

# Copy Google Drive sync integration
mkdir -p "$INCLUDES_ROOT/usr/lib/newbian/gdrive"
cp -r "$ROOT_DIR/packages/google-drive-sync/gdrive/"* "$INCLUDES_ROOT/usr/lib/newbian/gdrive/" 2>/dev/null || true
cp "$ROOT_DIR/packages/google-drive-sync/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp -r "$ROOT_DIR/packages/google-drive-sync/share/." "$INCLUDES_ROOT/usr/share/" 2>/dev/null || true
cp "$ROOT_DIR/packages/google-drive-sync/systemd/"* "$INCLUDES_ROOT/usr/lib/systemd/user/" 2>/dev/null || true

# Copy Figma integration
cp "$ROOT_DIR/packages/figma-integration/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/packages/figma-integration/share/applications/"* "$INCLUDES_ROOT/usr/share/applications/" 2>/dev/null || true
cp "$ROOT_DIR/packages/figma-integration/systemd/"* "$INCLUDES_ROOT/usr/lib/systemd/user/" 2>/dev/null || true

# Copy Interactive Installer & Branding
mkdir -p "$INCLUDES_ROOT/usr/lib/newbian/installer"
cp -r "$ROOT_DIR/installer/interactive-installer/"* "$INCLUDES_ROOT/usr/lib/newbian/installer/" 2>/dev/null || true
cp "$ROOT_DIR/installer/interactive-installer/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/installer/interactive-installer/share/applications/"* "$INCLUDES_ROOT/usr/share/applications/" 2>/dev/null || true

# Copy Custom Graphics & Wallpapers
mkdir -p "$INCLUDES_ROOT/usr/share/wallpapers/NewbianOS"
mkdir -p "$INCLUDES_ROOT/usr/share/icons/hicolor/scalable/apps"
cp "$ROOT_DIR/theme/wallpapers/"* "$INCLUDES_ROOT/usr/share/wallpapers/NewbianOS/" 2>/dev/null || true
cp "$ROOT_DIR/theme/icons/"* "$INCLUDES_ROOT/usr/share/icons/hicolor/scalable/apps/" 2>/dev/null || true

# Copy Theme & Skeleton
cp -r "$ROOT_DIR/theme/skel/." "$INCLUDES_ROOT/etc/skel/" 2>/dev/null || true

# Set execution permissions
chmod +x auto/config
chmod +x config/hooks/normal/*.hook.chroot 2>/dev/null || true
chmod +x "$INCLUDES_ROOT/usr/bin/"* 2>/dev/null || true

echo "⚙️  Configuring live-build recipe..."
lb clean
lb config

echo "🚀 Building NewbianOS live ISO image..."
lb build

ISO_OUTPUT=$(ls -1 "$BUILD_DIR"/*.iso 2>/dev/null | head -n 1 || true)
if [[ -n "$ISO_OUTPUT" ]]; then
    echo "🔧 Applying and verifying isohybrid MBR/GPT partition table for USB boot compatibility..."
    HYBRID_APPLIED=false

    if command -v isohybrid &>/dev/null; then
        if isohybrid --uefi "$ISO_OUTPUT" 2>/dev/null; then
            echo "✓ Isohybrid UEFI partition table applied successfully."
            HYBRID_APPLIED=true
        elif isohybrid "$ISO_OUTPUT" 2>/dev/null; then
            echo "✓ Isohybrid BIOS partition table applied successfully."
            HYBRID_APPLIED=true
        fi
    fi

    if [[ "$HYBRID_APPLIED" = false ]]; then
        echo "ℹ️ Checking if ISO already contains hybrid partition table from live-build/xorriso..."
        if fdisk -l "$ISO_OUTPUT" 2>/dev/null | grep -q -E "Disklabel type: (dos|gpt)"; then
            echo "✓ Valid partition table detected on ISO image."
            HYBRID_APPLIED=true
        else
            echo "⚠️  Applying hybrid partition table via xorriso fallback..."
            if command -v xorriso &>/dev/null; then
                xorriso -indev "$ISO_OUTPUT" -boot_image any replay -boot_image any isohybrid_mbr -outdev "${ISO_OUTPUT}.tmp" 2>/dev/null && mv "${ISO_OUTPUT}.tmp" "$ISO_OUTPUT" || true
            fi
        fi
    fi

    # Generate SHA-256 Checksum
    echo "🔒 Generating SHA-256 checksum..."
    (cd "$(dirname "$ISO_OUTPUT")" && sha256sum "$(basename "$ISO_OUTPUT")" > "$(basename "$ISO_OUTPUT").sha256")
    echo "✓ Checksum saved: ${ISO_OUTPUT}.sha256"

    # Display partition summary for verification
    if command -v fdisk &>/dev/null; then
        echo "📋 Partition Table Summary for BalenaEtcher & Rufus:"
        fdisk -l "$ISO_OUTPUT" 2>/dev/null || true
    fi

    if [[ -n "${SUDO_USER:-}" && "$SUDO_USER" != "root" ]]; then
        echo "🔒 Restoring build directory permissions to user $SUDO_USER..."
        chown -R "$SUDO_USER:$(id -gn "$SUDO_USER" 2>/dev/null || echo "$SUDO_USER")" "$ROOT_DIR/build" 2>/dev/null || true
    fi
    echo "======================================================================"
    echo "🎉 SUCCESS! NewbianOS ISO created at:"
    echo "   $ISO_OUTPUT"
    echo "   SHA256: $(cat "${ISO_OUTPUT}.sha256" | awk '{print $1}')"
    echo "   Ready for BalenaEtcher, Rufus, dd, and Ventoy USB creation."
    echo "======================================================================"
else
    echo "❌ Build completed without generating .iso. Check build logs."
    exit 1
fi
