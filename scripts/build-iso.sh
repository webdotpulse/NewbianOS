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
REQUIRED_TOOLS=("lb" "debootstrap" "xorriso" "grub-mkrescue" "mknod")
MISSING_TOOLS=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &>/dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [[ ${#MISSING_TOOLS[@]} -gt 0 ]]; then
    echo "⚠️  Missing build tools: ${MISSING_TOOLS[*]}"
    echo "   Installing build dependencies via apt..."
    apt-get update && apt-get install -y live-build debootstrap xorriso isolinux syslinux-efi grub-efi-amd64-bin
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
cp "$ROOT_DIR/packages/jarvis-assistant/systemd/"* "$INCLUDES_ROOT/usr/lib/systemd/user/" 2>/dev/null || true
cp "$ROOT_DIR/packages/jarvis-assistant/polkit/"* "$INCLUDES_ROOT/usr/share/polkit-1/actions/" 2>/dev/null || true

# Copy Google Chrome integration
cp "$ROOT_DIR/packages/google-chrome-integration/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/packages/google-chrome-integration/share/applications/"* "$INCLUDES_ROOT/usr/share/applications/" 2>/dev/null || true

# Copy Google Drive sync integration
mkdir -p "$INCLUDES_ROOT/usr/lib/newbian/gdrive"
cp -r "$ROOT_DIR/packages/google-drive-sync/gdrive/"* "$INCLUDES_ROOT/usr/lib/newbian/gdrive/" 2>/dev/null || true
cp "$ROOT_DIR/packages/google-drive-sync/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/packages/google-drive-sync/systemd/"* "$INCLUDES_ROOT/usr/lib/systemd/user/" 2>/dev/null || true

# Copy Figma integration
cp "$ROOT_DIR/packages/figma-integration/bin/"* "$INCLUDES_ROOT/usr/bin/" 2>/dev/null || true
cp "$ROOT_DIR/packages/figma-integration/share/applications/"* "$INCLUDES_ROOT/usr/share/applications/" 2>/dev/null || true
cp "$ROOT_DIR/packages/figma-integration/systemd/"* "$INCLUDES_ROOT/usr/lib/systemd/user/" 2>/dev/null || true

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
    echo "======================================================================"
    echo "🎉 SUCCESS! NewbianOS ISO created at:"
    echo "   $ISO_OUTPUT"
    echo "======================================================================"
else
    echo "❌ Build completed without generating .iso. Check build logs."
fi
