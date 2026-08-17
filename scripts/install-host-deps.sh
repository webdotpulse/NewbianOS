#!/usr/bin/env bash
# ==============================================================================
# Install Host Dependencies for Building NewbianOS
# ==============================================================================

set -eo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (sudo ./scripts/install-host-deps.sh)" 
   exit 1
fi

echo "📦 Installing required dependencies for NewbianOS development and ISO creation..."

apt-get update
apt-get install -y \
    debootstrap \
    debian-archive-keyring \
    xorriso \
    isolinux \
    syslinux-efi \
    syslinux-utils \
    grub-efi-amd64-bin \
    grub-pc-bin \
    grub-common \
    dosfstools \
    mtools \
    squashfs-tools \
    qemu-system-x86 \
    ovmf \
    python3 \
    python3-pip \
    desktop-file-utils \
    git \
    make \
    ca-certificates \
    gettext \
    po4a

# Ensure modern Debian live-build is installed
if ! command -v lb &>/dev/null || ! lb config --help 2>&1 | grep -q "iso-hybrid"; then
    echo "📦 Installing official modern live-build from salsa.debian.org..."
    TEMP_LB_DIR=$(mktemp -d)
    git clone --depth=1 https://salsa.debian.org/live-team/live-build.git "$TEMP_LB_DIR"
    (cd "$TEMP_LB_DIR" && make install)
    rm -rf "$TEMP_LB_DIR"
fi

echo "✓ All host dependencies installed successfully."
