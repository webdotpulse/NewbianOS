"""
Tests for Desktop Entries, Wayland Ozone Flags, and Theme Presets
"""

import os
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestDesktopIntegrations(unittest.TestCase):

    def test_desktop_entries_exist(self):
        """Verify presence of key desktop application entries."""
        antigravity_desktop = os.path.join(ROOT_DIR, "packages/antigravity-integration/share/applications/antigravity-ide.desktop")
        chrome_desktop = os.path.join(ROOT_DIR, "packages/google-chrome-integration/share/applications/google-chrome.desktop")
        figma_desktop = os.path.join(ROOT_DIR, "packages/figma-integration/share/applications/figma.desktop")

        self.assertTrue(os.path.exists(antigravity_desktop))
        self.assertTrue(os.path.exists(chrome_desktop))
        self.assertTrue(os.path.exists(figma_desktop))

    def test_ozone_flags_in_launchers(self):
        """Verify that launchers include Ozone Wayland flags."""
        launchers = [
            os.path.join(ROOT_DIR, "packages/antigravity-integration/bin/antigravity-ide"),
            os.path.join(ROOT_DIR, "packages/google-chrome-integration/bin/google-chrome-newbian"),
            os.path.join(ROOT_DIR, "packages/figma-integration/bin/figma-desktop")
        ]

        for l in launchers:
            with open(l, "r") as f:
                content = f.read()
                self.assertIn("--ozone-platform-hint=auto", content, f"Missing ozone flag in {l}")

    def test_starship_config(self):
        """Verify Starship prompt contains Antigravity and git configurations."""
        starship_path = os.path.join(ROOT_DIR, "theme/skel/.config/starship.toml")
        self.assertTrue(os.path.exists(starship_path))
        with open(starship_path, "r") as f:
            content = f.read()
            self.assertIn("custom.antigravity", content)
            self.assertIn("git_branch", content)

    def test_kwin_shortcuts(self):
        """Verify KWin shortcuts include Jarvis HUD and Antigravity."""
        kwin_path = os.path.join(ROOT_DIR, "theme/skel/.config/kwinrc")
        self.assertTrue(os.path.exists(kwin_path))
        with open(kwin_path, "r") as f:
            content = f.read()
            self.assertIn("jarvis_hud=Meta+Space", content)
            self.assertIn("antigravity_ide=Meta+A", content)

if __name__ == "__main__":
    unittest.main()
