# Building NewbianOS Live ISO

## Prerequisites
- A 64-bit x86_64 host running Debian, Ubuntu, or Debian-derived system.
- At least 20 GB of free disk space.
- Root or `sudo` privileges.

## Step 1: Install Build Dependencies
```bash
sudo ./scripts/install-host-deps.sh
```

## Step 2: Validate the Repository
```bash
make lint
make test
```

## Step 3: Generate the Live ISO
```bash
make iso
```
The resulting hybrid UEFI/BIOS bootable `.iso` file will be generated in `build/iso/`.

## Step 4: Test in Virtual Machine
```bash
make test-vm
```
This launches QEMU with KVM acceleration, 4GB RAM, UEFI (OVMF) firmware, and PipeWire audio.

## Step 5: Flash to USB Drive & Install
For detailed cross-platform flashing instructions (using **Ventoy**, **BalenaEtcher**, **Rufus**, or **dd** on Linux, Windows, and macOS), refer to:
👉 **[Creating an Installable USB Drive Manual](file:///home/koen/git/NewbianOS/docs/CREATE_USB_INSTALLER.md)**

Quick Linux CLI flash command:
```bash
sudo dd if=build/iso/NewbianOS-*.iso of=/dev/sdX bs=4M status=progress oflag=sync
```
*(Replace `/dev/sdX` with your target USB drive)*

---

## 🤖 Automated GitHub Release Builds
NewbianOS ISOs are automatically built and published as release assets on every tagged GitHub release via the GitHub Actions workflow in [`.github/workflows/release-iso.yml`](file:///home/koen/git/NewbianOS/.github/workflows/release-iso.yml). Pre-built ISOs and SHA-256 checksums can be downloaded directly from the GitHub Releases tab.

