# Jarvis Multimodal AI Assistant — Technical Architecture

```
                 +-----------------------------------+
                 |      Jarvis Multimodal Core       |
                 |             (jarvisd)             |
                 +-----------------+-----------------+
                                   |
         +-------------------------+-------------------------+
         |                         |                         |
+--------v--------+       +--------v--------+       +--------v--------+
|  Voice & Audio  |       |  Vision & NPU   |       |  OS Authority   |
| (PipeWire 3D)   |       | (OpenVINO/XDNA) |       | (Polkit/Atomic) |
+--------+--------+       +--------+--------+       +--------+--------+
         |                         |                         |
         +-------------------------+-------------------------+
                                   | IPC Socket (~/.jarvis/jarvis.sock) & D-Bus (org.newbianos.AgentEvents)
                   +---------------+---------------+
                   |                               |
           +-------v-------+               +-------v-------+
           |WebXR 3D HUD   |               |  Jarvis CLI   |
           | (jarvis-hud)  |               |   (jarvis)    |
           +---------------+               +---------------+
```

## 1. Multimodal Architecture

### A. NPU Neural Acceleration Engine (`jarvis.daemon.npu.manager`)
- **Hardware Abstraction Layer**: Native acceleration for Intel OpenVINO (IVPU), AMD Ryzen AI (XDNA), NVIDIA TensorRT-LLM, Qualcomm Hexagon, and Vulkan.
- **Quantization Loader**: Sub-10ms latency running 4-bit/8-bit quantized models (`GGUF Q4_K_M`, `ONNX-GenAI`, `AWQ`, `OpenVINO IR`).
- **Power Efficiency**: Offloads continuous wake-word listening and gaze tracking to the ultra-low-power NPU (2.4W draw).

### B. 3D Spatial Audio & Voice Macro Engine (`jarvis.daemon.voice`)
- **PipeWire 3D Spatial Audio**: Calculates binaural HRTF coordinates based on focused Wayland window geometry.
- **Voice Macro Shortcuts**: Maps voice gestures directly to developer operations (*"rebase on main and force push"*, *"split terminal and tail logs"*, *"swarm audit code"*, *"launch agy-box"*).
- **Speech Synthesis (TTS)**: Low-latency neural synthesis via Piper / OpenVINO.

### C. Optical Vision & PAM Face Biometrics (`jarvis.daemon.vision`, `jarvis.pam`)
- **V4L2 Optical Stream**: Face reticle, eye-gaze tracking, and distance sensing.
- **Zero-Trust PAM Module (`pam_jarvis_face`)**: Authenticates SDDM logins and passwordless `sudo` authorizations when the authorized developer is detected.

### D. Deep OS Execution Authority & Atomic Manager (`jarvis.daemon.executor`)
- **Polkit Privilege Helper**: Executes administrative tasks with security auditing.
- **Atomic Core & Snapper Rollbacks**: Instant 2-second rollback checkpoints via `newbian-rollback`.
- **Ephemeral Containers**: Disposable micro-container runtime via `agy-box` (`agy up`).

---

## 2. Holographic Spatial HUD (`jarvis-hud`)

The HUD provides a cyberpunk glassmorphic overlay featuring:
- **WebXR 3D Spatial Mode**: Interactive 6-DoF spatial canvas with perspective tilt and floating developer widgets.
- **Arc-Reactor Core**: Real-time pulsating core synchronized with PipeWire neural audio spectrum.
- **Live NPU & Swarm Telemetry**: Live TOPS, power draw, active quantized models, and background swarm status.
- **Optical Perception**: Target reticle and distance monitoring.

---

## 3. Terminal CLI Commands

```bash
# General intent execution & voice macros
jarvis "Restart nginx and reload systemd units"
jarvis "rebase on main and force push"

# Screen analysis & perception
jarvis --look
jarvis --status

# Swarm agent orchestration
agy-swarm spawn security "Audit all privileged sudo calls"
agy-swarm search "JarvisCoreDaemon"

# Instant Btrfs snapshots & rollbacks
newbian-rollback list
newbian-rollback rollback 1

# Ephemeral micro-containers
agy-box up
agy-box list

# Cloud workstation streaming
newbian-stream start 4k120
newbian-stream status

# Zero-trust hardware enclave
newbian-tpm-enclave status
newbian-tpm-enclave fido-sign
```
