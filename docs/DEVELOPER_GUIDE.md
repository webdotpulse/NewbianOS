# NewbianOS Developer Guide

## 1. Antigravity-IDE & AI Pair Programming
Antigravity-IDE is the default IDE in NewbianOS.

### Launching:
- Graphical shortcut: `Super + A`
- Command Line: `antigravity-ide .` or `agy chat`

### Pre-Configured Toolchains:
- **Node.js**: v22 LTS pre-installed with `npm`, `npx`, and `corepack` (pnpm / yarn).
- **Python**: Python 3.13 with `uv`, `poetry`, `pipx`, and virtualenv.
- **Containers**: Docker CE & Podman pre-configured with rootless permissions.
- **Git**: Configured with `delta` diff pager, syntax highlighting, Starship branch badges, and FIDO2 SSH signing (`git-fido-sign`).

---

## 2. Antigravity Multi-Agent Swarm & Code Graph (`agy-swarm`)
- **Semantic Code Graph Indexing**:
  ```bash
  agy index .
  agy search "function_name"
  ```
- **Autonomous Background Workers**:
  ```bash
  agy swarm spawn security "Audit all privileged calls"
  agy swarm spawn test "Fix failing unit tests"
  agy swarm spawn pr "Synthesize PR for current branch"
  ```

---

## 3. Ephemeral Micro-Containers (`agy-box`)
Run any project in disposable, isolated containers without polluting your host OS:
```bash
# Provision container with Wayland GUI, GPU & GoogleDrive pass-through
agy up

# List running container sandboxes (*.dev.local domains)
agy-box list

# Stop or destroy sandbox
agy-box destroy <BOX_ID>
```

---

## 4. Immutable Atomic Core & 2-Second Rollbacks (`newbian-rollback`)
NewbianOS isolates the system into transactional Btrfs subvolumes (`@`, `@home`, `@var`, `@snapshots`).
- **Create manual restore point**:
  ```bash
  newbian-rollback create "Pre-Kernel Upgrade"
  ```
- **List restore points**:
  ```bash
  newbian-rollback list
  ```
- **Instant Rollback**:
  ```bash
  newbian-rollback rollback 1
  ```
  *(Reboot to complete 2-second rollback directly from GRUB).*

---

## 5. Cloud Workstation & WebXR Spatial Streaming (`newbian-stream`)
Stream NewbianOS to thin clients, iPads, MacBooks, and VR/AR spatial headsets (Apple Vision Pro, Meta Quest):
```bash
# Start 4K 120fps AV1 streaming pipeline
newbian-stream start 4k120

# View connected clients and 6-DoF head pose metrics
newbian-stream clients
```

---

## 6. Zero-Trust Hardware Enclave & Face Unlock (`newbian-tpm-enclave`)
- **Optical Face Unlock (PAM)**: Unlock SDDM or authorize `sudo` by being present in front of the screen.
- **TPM2 Disk Enrollment**:
  ```bash
  newbian-tpm-enclave enroll-tpm /dev/nvme0n1p2
  ```
- **FIDO2 Hardware Key Git Signing**:
  ```bash
  newbian-tpm-enclave fido-sign developer@newbianos.org
  ```

---

## 7. Google Drive Workspace Sync (`~/GoogleDrive`)
All files saved in `~/GoogleDrive` are automatically synced to Google Cloud Workspace in the background:
- Check status: `gdrive status`
- Force sync: `gdrive sync`
- Dolphin Integration: Right-click any file in Dolphin to copy the Google Drive share link or sync instantly.

---

## 8. Figma Desktop & Local Font Helper
NewbianOS includes a local font daemon running on `127.0.0.1:18412` (`figma-font-helper`).
When using Figma in the browser or via `figma-desktop`, all installed developer fonts (JetBrains Mono, Inter, Fira Code, Roboto, Geist) are accessible on your canvas immediately without manual font uploads.
