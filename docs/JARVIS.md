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
|  Voice Engine   |       |  Vision Engine  |       |  OS Authority   |
| (PipeWire/TTS)  |       | (V4L2 / Screen) |       | (Polkit/System) |
+--------+--------+       +--------+--------+       +--------+--------+
         |                         |                         |
         +-------------------------+-------------------------+
                                   | IPC Socket (~/.jarvis/jarvis.sock)
                   +---------------+---------------+
                   |                               |
           +-------v-------+               +-------v-------+
           |Holographic HUD|               |  Jarvis CLI   |
           | (jarvis-hud)  |               |   (jarvis)    |
           +---------------+               +---------------+
```

## 1. Multimodal Architecture

### A. Voice Engine (`jarvis.daemon.voice.engine`)
- **Audio Capture**: Subscribes to PipeWire low-latency audio stream via `pw-cat` / `pw-record`.
- **Wake-Word Detection**: Continuous background listener for *"Hey Jarvis"*.
- **Speech-To-Text (STT)**: High-accuracy on-device transcription with Sherpa-ONNX / Whisper models.
- **Neural Speech Synthesis (TTS)**: Expressive neural voice output via Piper (`en_US-lessac-medium`) or system speech-dispatcher.
- **Reactive Audio Spectrum**: Computes real-time frequency spectrum bands (8 frequency bands) emitted over IPC to drive HUD audio visualizers.

### B. Optical Vision & Perception (`jarvis.daemon.vision.camera`)
- **V4L2 Camera Stream**: Captures video frames from `/dev/video0` or USB webcams.
- **Face & Eye-Gaze Tracking**: Computes bounding box `(x, y, width, height)`, gaze vector (`looking_at_code`, `looking_at_terminal`, `center`), and estimated distance in centimeters.
- **User Presence Awareness**: Automatically triggers greeting or low-power lock state based on user proximity.

### C. Screen Perception Sensor (`jarvis.daemon.vision.screen`)
- **Wayland PipeWire Screencast**: Captures desktop frame buffer through the FreeDesktop Desktop Portal (`org.freedesktop.portal.ScreenCast`).
- **Context Sensor**: Reads active window title, IDE file path, error traceback snippets, and active tech stack.

### D. Deep OS Execution Authority (`jarvis.daemon.executor.system_authority`)
- **Polkit Privilege Helper**: Configured with `/usr/share/polkit-1/actions/com.newbianos.jarvis.policy` to execute administrative tasks without plain password exposure.
- **Container Management**: Direct API for `docker` and `podman` lifecycle (`compose up`, `compose down`, `ps`, `logs`).
- **Service Management**: Controls user and system-level systemd units (`systemctl start/stop/restart/status`).
- **Hardware & Vitals Control**: Reads thermals, memory, CPU load, and controls audio volume and display backlight.

---

## 2. Holographic HUD (`jarvis-hud`)

The HUD provides a cyberpunk glassmorphism overlay featuring:
- Animated central Arc-Reactor core pulsing in sync with voice synthesis.
- Live audio spectrum waveform visualizer.
- Optical face-tracking target reticle with real-time coordinate badges.
- Live transcription subtitle stream and terminal command input field.
- Quick action triggers for container deployment, screen context analysis, system diagnostics, and Google Drive syncing.

---

## 3. Terminal CLI (`jarvis`)

```bash
# General intent execution
jarvis "Restart nginx and reload systemd units"

# Screen analysis
jarvis --look

# System vitals & perception
jarvis --status

# Speech output
jarvis --speak "Build completed with 0 errors."

# Open HUD overlay
jarvis --hud
```
