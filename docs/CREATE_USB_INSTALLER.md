# 💾 Creating an Installable NewbianOS USB Drive

This comprehensive guide provides step-by-step instructions for creating a bootable, installable USB flash drive from the **NewbianOS 13 Live ISO** image across **Linux**, **Windows**, and **macOS**.

---

## 📋 Quick Comparison of Methods

| Method | Recommended For | Operating Systems | Difficulty |
|---|---|---|---|
| **[Method 1: Ventoy](#-method-1-ventoy-recommended-multi-iso-drag--drop)** | **Highest Recommendation** (Multi-ISO, Drag & Drop) | Windows, Linux, macOS | ⭐ Easy |
| **[Method 2: BalenaEtcher](#-method-2-balenaetcher-or-raspberry-pi-imager-cross-platform-gui)** | Graphical one-click flash | Windows, Linux, macOS | ⭐ Easy |
| **[Method 3: Automated CLI (`make usb` / `create-usb.sh`)](#-method-3-newbianos-automated-usb-creator-cli)** | Safe Linux CLI with partition verification & device guard | Linux | ⭐ Easy |
| **[Method 4: Linux Terminal (`dd`)](#-method-4-linux-terminal-dd--manual-cli)** | Advanced Linux users & headless servers | Linux | ⚙️ Intermediate |
| **[Method 5: Rufus](#-method-5-windows-rufus-gui)** | Windows power users with partition control | Windows | ⚙️ Intermediate |
| **[Method 6: macOS Terminal (`dd`)](#-method-6-macos-terminal-dd)** | Native macOS command line | macOS | ⚙️ Intermediate |

---

## 🛠️ Prerequisites

1. **USB Flash Drive**: Minimum **8 GB** capacity (16 GB or higher USB 3.0+ recommended for fast boot and write speeds).
   > [!WARNING]
   > **All data currently on the USB drive will be permanently erased** during the flashing process (except with Ventoy once installed). Back up any important files before proceeding.
2. **NewbianOS ISO Image**: Download the latest release `.iso` from the [GitHub Releases](https://github.com/webdotpulse/NewbianOS/releases) page.
3. **Checksum File (`.sha256`)**: Downloaded alongside the ISO to verify image integrity.

---

## 🔍 Step 0: Verify ISO Integrity (SHA-256)

Before flashing, always verify that your downloaded ISO is not corrupted or truncated.

### Linux
```bash
# Check against the provided checksum file
sha256sum -c NewbianOS-13-Nexus-*.iso.sha256

# Or compute the hash manually
sha256sum NewbianOS-13-Nexus-*.iso
```
*Output should show: `NewbianOS-...-amd64.iso: OK`*

### macOS
```bash
shasum -a 256 NewbianOS-13-Nexus-*.iso
```

### Windows (PowerShell)
```powershell
Get-FileHash .\NewbianOS-13-Nexus-*.iso -Algorithm SHA256 | Format-List
```
Compare the output hash string with the contents of the `.sha256` file from GitHub Releases.

---

## 🚀 Method 1: Ventoy (Recommended: Multi-ISO Drag & Drop)

[Ventoy](https://www.ventoy.net/) is the most flexible and convenient tool for creating bootable USB media. You format the USB drive **only once**, and then you can copy and paste multiple ISOs directly onto the USB drive like normal files.

### Why Ventoy?
- Copy new NewbianOS ISO releases directly to the drive without reformatting.
- Keep other utilities, diagnostics, or Windows ISOs on the same drive.
- Supports both UEFI (GPT) and Legacy BIOS (MBR) out-of-the-box.

### Setup Instructions:

#### On Windows:
1. Download `ventoy-x.x.xx-windows.zip` from [Ventoy Releases](https://github.com/ventoy/Ventoy/releases).
2. Extract the archive and launch `Ventoy2Disk.exe`.
3. Select your USB drive from the **Device** dropdown.
4. *(Optional)* Click **Option** → **Partition Style** → Select **GPT** (recommended for modern UEFI systems).
5. Click **Install**. Confirm the prompts to format the USB.
6. Once completed, open File Explorer, navigate to the newly created `Ventoy` USB partition, and **copy/paste your `NewbianOS-*.iso` file** directly onto the drive.

#### On Linux:
```bash
# 1. Download and extract Ventoy
wget https://github.com/ventoy/Ventoy/releases/download/v1.0.99/ventoy-1.0.99-linux.tar.gz
tar -xzvf ventoy-*.tar.gz
cd ventoy-*/

# 2. Identify USB device name (e.g. /dev/sdb)
lsblk

# 3. Install Ventoy to the USB drive (WARNING: Replace /dev/sdX with your USB drive)
sudo sh Ventoy2Disk.sh -i -g /dev/sdX

# 4. Mount the Ventoy partition and copy the ISO
sudo mount /dev/sdX1 /mnt
sudo cp /path/to/NewbianOS-13-Nexus-*.iso /mnt/
sudo umount /mnt
sync
```

---

## 🎨 Method 2: BalenaEtcher or Raspberry Pi Imager (Cross-Platform GUI)

**BalenaEtcher** is an intuitive, foolproof graphical flashing utility available for Windows, macOS, and Linux.

1. Download and install **BalenaEtcher** from [etcher.balena.io](https://etcher.balena.io/) (or **Raspberry Pi Imager** from [raspberrypi.com/software](https://www.raspberrypi.com/software/)).
2. Insert your USB flash drive into your computer.
3. Open BalenaEtcher and follow the 3-step workflow:
   - **Flash from file**: Browse and select your downloaded `NewbianOS-13-Nexus-*.iso`.
   - **Select target**: Select your target USB drive (verify device size to avoid picking system drives).
   - **Flash!**: Click Flash and enter your system administrator password when prompted.
4. Wait for the flashing and verification pass to complete (typically 1–3 minutes on USB 3.0).
5. When finished, safely remove the USB drive.

> [!TIP]
> **BalenaEtcher Compatibility**:
> NewbianOS ISOs are built with hybrid MBR/GPT partition tables and UEFI ESP partitions. BalenaEtcher and Raspberry Pi Imager recognize NewbianOS ISOs directly without requiring special flags.

---

## ⚡ Method 3: NewbianOS Automated USB Creator CLI (`make usb` / `create-usb.sh`)

For Linux users who prefer a fast, safe command-line tool with built-in safety guards:

```bash
# 1. Connect your USB flash drive
# 2. Run the automated creator from the NewbianOS repository
make usb

# Or execute the script directly with explicit paths:
sudo ./scripts/create-usb.sh /path/to/NewbianOS-13-Nexus-v1.0.0-amd64.iso /dev/sdX
```

### Safety Features of `create-usb.sh`:
- **Auto-detection**: Automatically discovers USB flash drives and filters out internal SATA/NVMe drives.
- **Accidental Wipe Prevention**: Detects and refuses to write to partitions containing the host root filesystem (`/`).
- **Partition Correction**: Prevents targeting single partitions (e.g. `/dev/sdb1`) and guides writing to the whole drive (`/dev/sdb`).
- **Partition Table Verification**: Automatically re-reads the partition table (`partprobe`) and validates UEFI ESP and MBR tables.

---

## 🐧 Method 4: Linux Terminal (`dd` / Manual CLI)

The standard Unix `dd` utility provides raw, direct block writing. NewbianOS ISOs are built with `isohybrid` metadata, allowing them to boot natively when written as raw sector images.

### Step 1: Identify Your USB Drive
Plug in your USB drive and run:
```bash
lsblk -o NAME,SIZE,TYPE,TRAN,MODEL
```
Example output:
```
NAME   SIZE TYPE TRAN   MODEL
sda    1.8T disk sata   Samsung_SSD_870
sdb   29.8G disk usb    SanDisk_Ultra   <--- Target device: /dev/sdb
```
> [!CAUTION]
> **Double check your device letter!** Writing to the wrong disk (e.g., `/dev/sda` or `/dev/nvme0n1`) will destroy your host system installation. Never target a partition number (e.g. `/dev/sdb1`), always target the raw whole disk (e.g. `/dev/sdb`).

### Step 2: Unmount Existing Partitions
If the operating system auto-mounted the USB drive:
```bash
sudo umount /dev/sdX* 2>/dev/null || true
```
*(Replace `sdX` with your target device, e.g. `sdb`)*

### Step 3: Write the ISO Image
```bash
sudo dd if=NewbianOS-13-Nexus-v1.0.0-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

### Step 4: Flush Cache & Eject
```bash
sync
sudo eject /dev/sdX
```

---

## 🪟 Method 5: Windows (Rufus GUI)

[Rufus](https://rufus.ie/) is a lightweight, reliable USB flashing utility for Windows.

1. Download **Rufus Portable** from [rufus.ie](https://rufus.ie/).
2. Insert your USB flash drive and launch Rufus (run as Administrator).
3. Configure the following options:
   - **Device**: Select your USB flash drive.
   - **Boot selection**: Click **SELECT** and choose `NewbianOS-13-Nexus-*.iso`.
   - **Partition scheme**: Select **GPT** (for modern UEFI computers) or **MBR** (for older BIOS/Legacy systems).
   - **Target system**: Select **UEFI (non CSM)**.
   - **Volume label**: Defaults to `NEWBIAN_13_DEV`.
   - **File system**: Leave as `FAT32` or default.
4. Click **START**.
5. > [!IMPORTANT]
   > **When prompted with the "ISOHybrid image detected" modal**:
   > Select **"Write in DD Image mode"** and click **OK**.
   > *(DD Image mode guarantees that all boot sectors, EFI partitions, and SquashFS live overlays are written identically to the Linux disk layout).*
6. Confirm the warning that all existing data will be wiped.
7. Wait until the status bar reaches 100% (**READY**).

---

## 🍎 Method 6: macOS Terminal (`dd`)

1. Open **Terminal** on macOS (`Command + Space` → Terminal).
2. List storage disks before and after plugging in your USB:
   ```bash
   diskutil list
   ```
   Identify your USB identifier (e.g. `/dev/disk4`).
3. Unmount the USB disk:
   ```bash
   diskutil unmountDisk /dev/diskN
   ```
   *(Replace `diskN` with your USB disk number, e.g. `disk4`)*
4. Write the ISO using the raw disk device (`rdiskN` for optimal transfer speed):
   ```bash
   sudo dd if=NewbianOS-13-Nexus-*.iso of=/dev/rdiskN bs=4m status=progress
   ```
5. Once completed, eject the drive:
   ```bash
   diskutil eject /dev/diskN
   ```

---

## 💻 Booting into NewbianOS

### 1. Access the BIOS/UEFI Boot Menu
1. Turn off your target computer.
2. Insert the NewbianOS bootable USB drive into a high-speed USB port (preferably directly on the motherboard / chassis).
3. Power on the machine and immediately tap the **Boot Menu Key** repeatedly until the boot selection menu appears:

| Manufacturer | Typical Boot Menu Key | BIOS / UEFI Setup Key |
|---|---|---|
| **Dell / Alienware** | `F12` | `F2` |
| **Lenovo / ThinkPad** | `F12` or `Fn + F12` (or Novo Button) | `F1` or `Enter` |
| **HP / Omen** | `F9` or `Esc` → `F9` | `F10` or `Esc` |
| **ASUS / ROG** | `F8` or `Esc` | `Del` or `F2` |
| **MSI** | `F11` | `Del` |
| **Acer / Predator** | `F12` | `F2` |
| **Gigabyte / AORUS** | `F12` | `Del` |
| **Apple Mac (Intel)** | Hold `Option` (`Alt`) on power-up | `Command + R` |
| **Custom PC / Framework** | `F12` or `Del` | `Del` or `F2` |

### 2. Select the USB Drive
From the boot menu list, select:
- **`UEFI: [USB Drive Name], Partition 1`** (Recommended)

### 3. Choose GRUB Live Menu Option
The NewbianOS GRUB bootloader will present the following options:
1. **⚡ NewbianOS 13 Live (KDE Plasma 6 / Wayland)**: Standard high-performance developer live session with full hardware acceleration.
2. **⚡ NewbianOS 13 Live (Safe Graphics / nomodeset)**: Use this if you have bleeding-edge or unsupported discrete GPUs causing a black screen.
3. **⚡ Install NewbianOS Directly**: Boot straight into the installer.

---

## ⚡ Starting the Installer in Live Session

Once the KDE Plasma 6 desktop loads:
1. Click the **"Install NewbianOS"** icon on the desktop or Application Launcher.
2. Or open terminal (`Super + T`) and launch:
   ```bash
   newbian-installer
   ```
3. Follow the installation wizard to configure your locale, keyboard, user accounts, and Btrfs subvolumes (`@`, `@home`, `@snapshots`).

---

## ❓ Troubleshooting & FAQs

### Q1: The USB drive does not appear in the UEFI Boot Menu.
- **Solution A**: Ensure **Fast Startup** is disabled in Windows if dual-booting.
- **Solution B**: In your BIOS settings, ensure **USB Boot Support** is Enabled.
- **Solution C**: Try plugging into a USB 2.0 / USB 3.0 port directly on the motherboard rather than via an unpowered USB hub.

### Q2: Black screen or freeze after selecting GRUB boot option.
- **Solution**: Restart and select **`NewbianOS 13 Live (Safe Graphics / nomodeset)`**. Once installed, proprietary NVIDIA or custom GPU drivers can be managed via the driver manager.

### Q3: Rufus gave an error about missing files.
- **Solution**: Make sure you selected **"Write in DD Image mode"** when prompted by Rufus. If ISO mode was selected, re-flash using DD mode or use **Ventoy**.

### Q4: BalenaEtcher warns "Missing partition table - It looks like this is not a bootable image".
- **Why it happens**: BalenaEtcher scans sector 0 for a raw partition table (MBR/GPT). Standard optical disc ISOs rely on El Torito catalog records rather than standard hard disk partition tables.
- **Solution A (Click Continue)**: Click **"Continue"** in BalenaEtcher. The image will flash and modern UEFI computers will recognize the EFI bootloader.
- **Solution B (Convert ISO with `isohybrid`)**: Convert the ISO into a hybrid disk image with an embedded MBR/GPT partition table before opening in Etcher:
  ```bash
  sudo apt-get install syslinux-utils
  isohybrid --uefi /path/to/NewbianOS-*.iso
  ```
  Once converted, BalenaEtcher will accept the ISO immediately without warnings.
- **Solution C (Use Ventoy or Rufus)**: Use **Ventoy** (Method 1) or **Rufus** (Method 4) which automatically support booting ISO files directly.

### Q5: How do I restore my USB drive back to normal storage afterwards?
- **Windows**: Open `diskpart` → `list disk` → `select disk X` → `clean` → `create partition primary` → `format fs=ntfs quick`.
- **Linux**: Use GNOME Disks or `sudo wipefs -a /dev/sdX && sudo parted -s /dev/sdX mklabel gpt mkpart primary fat32 1MiB 100% && sudo mkfs.vfat -F32 /dev/sdX1`.
- **macOS**: Open **Disk Utility** → Select USB Drive → Click **Erase** → Format as `ExFAT` or `MS-DOS (FAT)`.
