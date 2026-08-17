#!/usr/bin/env bash
# ==============================================================================
# NewbianOS QEMU/KVM Virtual Machine Live ISO Test Runner
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

ISO_PATH="${1:-}"

if [[ -z "$ISO_PATH" ]]; then
    # Try finding latest ISO in build directory
    ISO_PATH=$(ls -t "$ROOT_DIR/build/iso/"*.iso 2>/dev/null | head -n 1 || true)
fi

if [[ -z "$ISO_PATH" || ! -f "$ISO_PATH" ]]; then
    echo "⚠️  No ISO image found. Please provide path to ISO or build one using: make iso"
    echo "Usage: ./scripts/test-vm.sh [path/to/newbianos.iso]"
    exit 1
fi

echo "======================================================================"
echo "⚡ Launching NewbianOS Live ISO in QEMU/KVM..."
echo "   ISO: $ISO_PATH"
echo "======================================================================"

QEMU_BIN="qemu-system-x86_64"
if ! command -v "$QEMU_BIN" &>/dev/null; then
    echo "❌ Error: $QEMU_BIN is not installed. Please install qemu-system-x86."
    exit 1
fi

# Detect KVM hardware virtualization support
KVM_FLAGS=()
if [[ -r /dev/kvm ]] && grep -Eq '(vmx|svm)' /proc/cpuinfo 2>/dev/null; then
    echo "✓ KVM Hardware Acceleration enabled."
    KVM_FLAGS+=("-enable-kvm" "-cpu" "host")
else
    echo "⚠️  KVM not available. Running in emulation mode."
    KVM_FLAGS+=("-cpu" "max")
fi

# Locate UEFI firmware (OVMF)
OVMF_CODE=""
for candidate in "/usr/share/OVMF/OVMF_CODE.fd" "/usr/share/ovmf/OVMF.fd" "/usr/share/edk2-ovmf/x64/OVMF_CODE.fd"; do
    if [[ -f "$candidate" ]]; then
        OVMF_CODE="$candidate"
        break
    fi
done

BIOS_FLAGS=()
if [[ -n "$OVMF_CODE" ]]; then
    echo "✓ UEFI / OVMF firmware loaded from: $OVMF_CODE"
    BIOS_FLAGS+=("-bios" "$OVMF_CODE")
fi

exec "$QEMU_BIN" \
    "${KVM_FLAGS[@]}" \
    "${BIOS_FLAGS[@]}" \
    -m 4096 \
    -smp 4 \
    -vga virtio \
    -display default,show-cursor=on \
    -audiodev id=snd0,driver=pa \
    -device intel-hda \
    -device hda-duplex,audiodev=snd0 \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::2222-:22 \
    -cdrom "$ISO_PATH" \
    -boot d
