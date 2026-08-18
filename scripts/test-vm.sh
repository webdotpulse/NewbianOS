#!/usr/bin/env bash
# ==============================================================================
# NewbianOS QEMU/KVM Virtual Machine Live ISO & USB Test Runner
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

USE_USB=false
USE_BIOS=false
ISO_PATH=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --usb|-u)
            USE_USB=true
            shift
            ;;
        --legacy|--bios|-b)
            USE_BIOS=true
            shift
            ;;
        --help|-h)
            echo "Usage: ./scripts/test-vm.sh [OPTIONS] [path/to/newbianos.iso]"
            echo ""
            echo "Options:"
            echo "  --usb, -u       Emulate USB 3.0 flash drive boot instead of CD-ROM"
            echo "  --legacy, -b    Emulate Legacy BIOS mode instead of UEFI"
            echo "  --help, -h      Show this help message"
            exit 0
            ;;
        *)
            if [[ -z "$ISO_PATH" ]]; then
                ISO_PATH="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$ISO_PATH" ]]; then
    # Try finding latest ISO in build directory
    ISO_PATH=$(ls -t "$ROOT_DIR/build/iso/"*.iso 2>/dev/null | head -n 1 || true)
    if [[ -z "$ISO_PATH" ]]; then
        ISO_PATH=$(ls -t "$ROOT_DIR/"*.iso 2>/dev/null | head -n 1 || true)
    fi
fi

if [[ -z "$ISO_PATH" || ! -f "$ISO_PATH" ]]; then
    echo "⚠️  No ISO image found. Please provide path to ISO or build one using: make iso"
    echo "Usage: ./scripts/test-vm.sh [--usb] [--legacy] [path/to/newbianos.iso]"
    exit 1
fi

echo "======================================================================"
echo "⚡ Launching NewbianOS in QEMU/KVM Virtual Machine..."
echo "   ISO: $ISO_PATH"
echo "   Mode: $([ "$USE_USB" = true ] && echo "USB 3.0 Flash Drive" || echo "Optical CD-ROM")"
echo "   Firmware: $([ "$USE_BIOS" = true ] && echo "Legacy BIOS" || echo "UEFI (OVMF)")"
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

# Locate UEFI firmware (OVMF) if not legacy BIOS
FIRMWARE_FLAGS=()
if [[ "$USE_BIOS" = false ]]; then
    OVMF_CODE=""
    for candidate in "/usr/share/OVMF/OVMF_CODE.fd" "/usr/share/ovmf/OVMF.fd" "/usr/share/edk2-ovmf/x64/OVMF_CODE.fd"; do
        if [[ -f "$candidate" ]]; then
            OVMF_CODE="$candidate"
            break
        fi
    done

    if [[ -n "$OVMF_CODE" ]]; then
        echo "✓ UEFI / OVMF firmware loaded from: $OVMF_CODE"
        FIRMWARE_FLAGS+=("-bios" "$OVMF_CODE")
    else
        echo "⚠️  OVMF UEFI firmware not found on host. Falling back to BIOS mode."
    fi
fi

# Configure Storage & Boot Medium (CD-ROM vs USB Mass Storage)
STORAGE_FLAGS=()
if [[ "$USE_USB" = true ]]; then
    echo "✓ Attaching ISO as Emulated USB 3.0 Mass Storage Device..."
    STORAGE_FLAGS+=(
        "-drive" "if=none,id=usbstick,format=raw,file=$ISO_PATH"
        "-device" "qemu-xhci,id=xhci"
        "-device" "usb-storage,bus=xhci.0,drive=usbstick,bootindex=1"
    )
else
    STORAGE_FLAGS+=(
        "-cdrom" "$ISO_PATH"
        "-boot" "d"
    )
fi

exec "$QEMU_BIN" \
    "${KVM_FLAGS[@]}" \
    "${FIRMWARE_FLAGS[@]}" \
    "${STORAGE_FLAGS[@]}" \
    -m 4096 \
    -smp 4 \
    -vga virtio \
    -display default,show-cursor=on \
    -audiodev id=snd0,driver=pa \
    -device intel-hda \
    -device hda-duplex,audiodev=snd0 \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::2222-:22
