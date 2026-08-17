"""
Tests for CI/CD Workflows, ISO Release Automation, and USB Documentation
"""

import os
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestCIAndDocumentation(unittest.TestCase):

    def test_release_workflow_exists_and_configured(self):
        """Verify .github/workflows/release-iso.yml triggers on release and builds ISO."""
        workflow_path = os.path.join(ROOT_DIR, ".github/workflows/release-iso.yml")
        self.assertTrue(os.path.exists(workflow_path), "Missing release-iso.yml workflow")

        with open(workflow_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check triggers
        self.assertIn("release:", content)
        self.assertIn("types: [published]", content)
        self.assertIn("workflow_dispatch:", content)

        # Check key actions and steps
        self.assertIn("actions/checkout@v4", content)
        self.assertIn("live-build", content)
        self.assertIn("build-iso.sh", content)
        self.assertIn("sha256sum", content)
        self.assertIn("softprops/action-gh-release", content)

    def test_ci_workflow_exists(self):
        """Verify .github/workflows/ci.yml exists and runs lint/test suites."""
        ci_path = os.path.join(ROOT_DIR, ".github/workflows/ci.yml")
        self.assertTrue(os.path.exists(ci_path), "Missing ci.yml workflow")

        with open(ci_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("push:", content)
        self.assertIn("pull_request:", content)
        self.assertIn("make lint", content)
        self.assertIn("make test", content)

    def test_usb_creation_guide_exists_and_complete(self):
        """Verify docs/CREATE_USB_INSTALLER.md contains all cross-platform flashing guides."""
        guide_path = os.path.join(ROOT_DIR, "docs/CREATE_USB_INSTALLER.md")
        self.assertTrue(os.path.exists(guide_path), "Missing CREATE_USB_INSTALLER.md")

        with open(guide_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check essential methods and tools
        self.assertIn("Ventoy", content)
        self.assertIn("BalenaEtcher", content)
        self.assertIn("dd", content)
        self.assertIn("Rufus", content)
        self.assertIn("diskutil", content)
        self.assertIn("DD Image mode", content)
        self.assertIn("sha256sum", content)
        self.assertIn("Boot Menu", content)
        self.assertIn("Troubleshooting", content)

    def test_install_host_deps_packages(self):
        """Verify scripts/install-host-deps.sh installs correct debian packages."""
        script_path = os.path.join(ROOT_DIR, "scripts/install-host-deps.sh")
        self.assertTrue(os.path.exists(script_path))

        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("live-build", content)
        self.assertIn("xorriso", content)
        self.assertIn("squashfs-tools", content)
        # Ensure non-existent package mknod is not in apt install list
        self.assertNotIn("mknod \\", content)

if __name__ == "__main__":
    unittest.main()
