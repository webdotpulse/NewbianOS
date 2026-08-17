"""
PipeWire 3D Spatial Audio & Binaural HRTF Positioning Engine
Dynamically positions Jarvis audio output in 3D virtual auditory space aligned with focused Wayland windows.
"""

import math
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger("jarvis.spatial_audio")

@dataclass
class SpatialPosition3D:
    x: float  # -1.0 (far left) to +1.0 (far right)
    y: float  # -1.0 (below) to +1.0 (above)
    z: float  # distance in meters (default 0.8m)
    azimuth_deg: float  # -90° (left) to +90° (right)
    elevation_deg: float  # -45° to +45°
    gain: float

class SpatialAudioEngine:
    def __init__(self, screen_width: int = 1920, screen_height: int = 1080):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.binaural_hrtf_enabled = True

    def calculate_window_spatial_position(self, window_rect: Optional[Dict[str, int]] = None) -> SpatialPosition3D:
        """
        Calculate 3D binaural audio coordinates for an active window.
        window_rect: {"x": int, "y": int, "w": int, "h": int}
        """
        if not window_rect:
            # Default center auditory position
            return SpatialPosition3D(
                x=0.0,
                y=0.0,
                z=0.8,
                azimuth_deg=0.0,
                elevation_deg=0.0,
                gain=1.0
            )

        win_center_x = window_rect.get("x", self.screen_width // 2) + window_rect.get("w", 800) // 2
        win_center_y = window_rect.get("y", self.screen_height // 2) + window_rect.get("h", 600) // 2

        # Normalize to [-1.0, 1.0]
        norm_x = (win_center_x / self.screen_width) * 2.0 - 1.0
        norm_y = 1.0 - (win_center_y / self.screen_height) * 2.0  # Invert Y so up is positive

        # Clamp
        norm_x = max(-1.0, min(1.0, norm_x))
        norm_y = max(-1.0, min(1.0, norm_y))

        azimuth = norm_x * 45.0  # Up to 45 degrees left or right
        elevation = norm_y * 20.0 # Up to 20 degrees up or down

        return SpatialPosition3D(
            x=round(norm_x, 2),
            y=round(norm_y, 2),
            z=0.75,
            azimuth_deg=round(azimuth, 1),
            elevation_deg=round(elevation, 1),
            gain=1.0
        )

    def generate_pipewire_spatial_args(self, pos: SpatialPosition3D) -> list:
        """Generate PipeWire pw-play / filter-chain spatializer properties."""
        # Convert azimuth to stereo pan balance [-1.0 to +1.0]
        pan = pos.x
        left_gain = math.cos((pan + 1.0) * (math.pi / 4.0))
        right_gain = math.sin((pan + 1.0) * (math.pi / 4.0))

        return [
            "--property", f"spatial.position.x={pos.x}",
            "--property", f"spatial.position.y={pos.y}",
            "--property", f"spatial.position.z={pos.z}",
            "--property", f"spatial.azimuth={pos.azimuth_deg}",
            "--property", f"stream.volume-left={left_gain:.2f}",
            "--property", f"stream.volume-right={right_gain:.2f}"
        ]
