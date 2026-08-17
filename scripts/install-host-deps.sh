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
    live-build \
    debootstrap \
    xorriso \
    isolinux \
    syslinux-efi \
    grub-efi-amd64-bin \
    grub-pc-bin \
    mknod \
    dosfstools \
    mtools \
    qemu-system-x86 \
    ovmf \
    python3 \
    python3-pip \
    desktop-file-utils

echo "✓ All host dependencies installed successfully."
