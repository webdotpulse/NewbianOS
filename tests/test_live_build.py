"""
Tests for Live Build Package Lists and Configuration
"""

import os
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestLiveBuildConfig(unittest.TestCase):

    def test_package_lists_exist(self):
        """Verify presence and validity of live-build package lists."""
        pkg_lists = [
            "iso-builder/config/package-lists/desktop-kde.list.chroot",
            "iso-builder/config/package-lists/developer-core.list.chroot",
            "iso-builder/config/package-lists/multimedia-hardware.list.chroot",
            "iso-builder/config/package-lists/apps-standard.list.chroot"
        ]

        for p in pkg_lists:
            full_path = os.path.join(ROOT_DIR, p)
            self.assertTrue(os.path.exists(full_path), f"Missing package list: {p}")
            with open(full_path, "r") as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
                self.assertTrue(len(lines) > 5, f"Package list {p} should have multiple packages")

    def test_minimal_kde_packages(self):
        """Verify that KDE desktop packages are minimal and exclude bloatware."""
        kde_list_path = os.path.join(ROOT_DIR, "iso-builder/config/package-lists/desktop-kde.list.chroot")
        with open(kde_list_path, "r") as f:
            content = f.read()
            # Essential components must exist
            self.assertIn("plasma-workspace-wayland", content)
            self.assertIn("dolphin", content)
            self.assertIn("konsole", content)
            # Bloatware must NOT be included
            self.assertNotIn("kate\n", content)
            self.assertNotIn("kwrite\n", content)
            self.assertNotIn("gwenview\n", content)
            self.assertNotIn("okular\n", content)
            self.assertNotIn("kcalc\n", content)

    def test_auto_config(self):
        """Verify auto/config file targets trixie and amd64."""
        auto_config_path = os.path.join(ROOT_DIR, "iso-builder/auto/config")
        self.assertTrue(os.path.exists(auto_config_path))
        with open(auto_config_path, "r") as f:
            content = f.read()
            self.assertIn("--distribution trixie", content)
            self.assertIn("--architectures amd64", content)
            self.assertIn("--system live", content)
            self.assertIn("--initsystem systemd", content)

    def test_chroot_hooks(self):
        """Verify chroot hooks are present."""
        hooks = [
            "01-hardware-acceleration.hook.chroot",
            "02-shell-starship.hook.chroot",
            "03-services-enable.hook.chroot",
            "04-calamares-branding.hook.chroot",
            "05-desktop-defaults.hook.chroot",
            "06-npu-acceleration.hook.chroot",
            "07-btrfs-snapper.hook.chroot",
            "08-pam-biometrics.hook.chroot"
        ]
        for h in hooks:
            hook_path = os.path.join(ROOT_DIR, "iso-builder/config/hooks/normal", h)
            self.assertTrue(os.path.exists(hook_path), f"Missing hook: {h}")

    def test_kernel_v7_pinning(self):
        """Verify Kernel v7+ APT preference pinning exists and is valid."""
        pref_path = os.path.join(ROOT_DIR, "iso-builder/config/includes.chroot/etc/apt/preferences.d/kernel-v7.pref")
        self.assertTrue(os.path.exists(pref_path), "Missing kernel-v7.pref")
        with open(pref_path, "r") as f:
            content = f.read()
            self.assertIn("Pin: version 7.*", content)

        # Check multimedia-hardware list contains linux-image-amd64 and cpupower
        pkg_path = os.path.join(ROOT_DIR, "iso-builder/config/package-lists/multimedia-hardware.list.chroot")
        with open(pkg_path, "r") as f:
            pkg_content = f.read()
            self.assertIn("linux-image-amd64", pkg_content)
            self.assertIn("linux-headers-amd64", pkg_content)

if __name__ == "__main__":
    unittest.main()
