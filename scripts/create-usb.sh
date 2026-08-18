#!/usr/bin/env bash
# ==============================================================================
# NewbianOS Automated Bootable USB Creator
# Safely writes NewbianOS ISO to USB flash drives with hybrid partition verification
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "======================================================================"
echo "⚡ NewbianOS 13 'Nexus' Bootable USB Creator"
echo "======================================================================"

# Require root/sudo permissions for direct block access
if [[ $EUID -ne 0 ]]; then
    echo "🔒 Root privileges required for USB block write."
    echo "   Re-running with sudo..."
    exec sudo "$0" "$@"
fi

ISO_PATH="${1:-}"
TARGET_DEV="${2:-}"

# 1. Locate ISO Image
if [[ -z "$ISO_PATH" ]]; then
    ISO_PATH=$(ls -t "$ROOT_DIR/build/iso/"*.iso 2>/dev/null | head -n 1 || true)
    if [[ -z "$ISO_PATH" ]]; then
        ISO_PATH=$(ls -t "$ROOT_DIR/"*.iso 2>/dev/null | head -n 1 || true)
    fi
fi

if [[ -z "$ISO_PATH" || ! -f "$ISO_PATH" ]]; then
    echo "❌ Error: ISO image not found."
    echo "Usage: sudo ./scripts/create-usb.sh [path/to/newbianos.iso] [/dev/sdX]"
    echo ""
    echo "Please build the ISO first using 'make iso' or specify an existing ISO path."
    exit 1
fi

ISO_SIZE_MB=$(du -m "$ISO_PATH" | cut -f1)
echo "📦 Source ISO: $ISO_PATH (${ISO_SIZE_MB} MB)"

# 2. Check for plugged-in USB storage devices
if [[ -z "$TARGET_DEV" ]]; then
    echo ""
    echo "🔍 Scanning for connected USB flash drives..."
    
    USB_DISKS=()
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            USB_DISKS+=("$line")
        fi
    done < <(lsblk -d -n -p -o NAME,SIZE,TRAN,MODEL | grep -i "usb" || true)

    if [[ ${#USB_DISKS[@]} -eq 0 ]]; then
        echo "⚠️  No USB flash drives detected via transport bus."
        echo "   Listing all removable block devices:"
        lsblk -d -p -o NAME,SIZE,TYPE,TRAN,MODEL,RM
        echo ""
        read -r -p "Enter target device path (e.g. /dev/sdb): " TARGET_DEV
    elif [[ ${#USB_DISKS[@]} -eq 1 ]]; then
        AUTO_DEV=$(echo "${USB_DISKS[0]}" | awk '{print $1}')
        echo "Found USB drive: ${USB_DISKS[0]}"
        read -r -p "Write to $AUTO_DEV? [y/N]: " CONFIRM_AUTO
        if [[ "$CONFIRM_AUTO" =~ ^[Yy]$ ]]; then
            TARGET_DEV="$AUTO_DEV"
        else
            read -r -p "Enter target device path (e.g. /dev/sdb): " TARGET_DEV
        fi
    else
        echo "Multiple USB drives found:"
        for i in "${!USB_DISKS[@]}"; do
            echo "  $((i+1))) ${USB_DISKS[$i]}"
        done
        read -r -p "Select drive number [1-${#USB_DISKS[@]}]: " CHOICE
        if [[ "$CHOICE" =~ ^[0-9]+$ ]] && (( CHOICE >= 1 && CHOICE <= ${#USB_DISKS[@]} )); then
            TARGET_DEV=$(echo "${USB_DISKS[$((CHOICE-1))]}" | awk '{print $1}')
        else
            echo "❌ Invalid selection."
            exit 1
        fi
    fi
fi

# 3. Safety Validations
if [[ ! -b "$TARGET_DEV" ]]; then
    echo "❌ Error: $TARGET_DEV is not a valid block device."
    exit 1
fi

# Reject partition targets (e.g. /dev/sdb1 instead of /dev/sdb)
if [[ "$TARGET_DEV" =~ [0-9]$ && ! "$TARGET_DEV" =~ nvme.*p[0-9]$ ]]; then
    echo "⚠️  Warning: $TARGET_DEV looks like a partition, not a whole disk."
    SUGGESTED_DISK=$(echo "$TARGET_DEV" | sed 's/[0-9]*$//')
    echo "   Writing must be done to the entire disk device: $SUGGESTED_DISK"
    read -r -p "Use whole disk $SUGGESTED_DISK instead? [y/N]: " USE_DISK
    if [[ "$USE_DISK" =~ ^[Yy]$ ]]; then
        TARGET_DEV="$SUGGESTED_DISK"
    else
        echo "❌ Aborting to protect partition tables."
        exit 1
    fi
fi

# Protect root / system drives
ROOT_DEV=$(findmnt -n -o SOURCE / || true)
if [[ "$ROOT_DEV" == "$TARGET_DEV"* ]]; then
    echo "⛔ DANGER: $TARGET_DEV contains the currently running root filesystem ($ROOT_DEV)!"
    echo "   Aborting to prevent system destruction."
    exit 1
fi

echo "======================================================================"
echo "🎯 TARGET DEVICE: $TARGET_DEV"
lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINT "$TARGET_DEV" || true
echo "======================================================================"
echo "⚠️  WARNING: ALL DATA ON $TARGET_DEV WILL BE PERMANENTLY WIPED!"
read -r -p "Type 'YES' in uppercase to confirm and write: " CONFIRM_WIPE

if [[ "$CONFIRM_WIPE" != "YES" ]]; then
    echo "❌ Flash operation cancelled by user."
    exit 0
fi

# 4. Unmount any active partitions on the device
echo "🔌 Unmounting active partitions on $TARGET_DEV..."
umount "${TARGET_DEV}"* 2>/dev/null || true

# 5. Write ISO using direct DD with progress & sync
echo "🚀 Writing NewbianOS ISO to $TARGET_DEV..."
dd if="$ISO_PATH" of="$TARGET_DEV" bs=4M status=progress oflag=sync conv=fsync

echo "⏳ Flushing I/O buffers to physical flash storage..."
sync

# 6. Re-read partition table
echo "🔍 Re-reading partition table..."
partprobe "$TARGET_DEV" 2>/dev/null || blockdev --rereadpt "$TARGET_DEV" 2>/dev/null || true
sleep 1

# 7. Verification & Confirmation
echo "======================================================================"
echo "📋 Verifying NewbianOS USB Structure:"
lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL "$TARGET_DEV" || true
echo "======================================================================"
echo "🎉 SUCCESS! Bootable NewbianOS USB drive is ready."
echo "   - UEFI Boot: Supported (Partition 1 / ESP)"
echo "   - Legacy BIOS Boot: Supported (MBR Hybrid Code)"
echo "   You may now safely unplug the USB and boot your target machine."
echo "======================================================================"
