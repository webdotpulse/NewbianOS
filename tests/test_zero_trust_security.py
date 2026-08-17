"""
Unit & Integration Tests for Zero-Trust Hardware Enclave & Jarvis Face Unlock
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/jarvis-assistant")))

from jarvis.pam.pam_jarvis_face import JarvisBiometricAuthenticator, PamAuthResult
from jarvis.daemon.security.enclave import HardwareEnclaveManager, TPM2Status

class TestZeroTrustSecurity(unittest.TestCase):

    def setUp(self):
        self.auth = JarvisBiometricAuthenticator()
        self.enclave = HardwareEnclaveManager()

    def test_biometric_face_verification_success(self):
        """Verify successful biometric verification with nominal perception."""
        perception = {
            "user_present": True,
            "face": {"x": 50, "y": 50, "w": 60, "h": 70},
            "distance_cm": 65.0,
            "gaze": "center"
        }
        res = self.auth.verify_user("developer", perception)
        self.assertTrue(res.authenticated)
        self.assertGreaterEqual(res.confidence_score, 0.88)
        self.assertTrue(res.gaze_aligned)

        pam_status = self.auth.pam_sm_authenticate("developer", perception)
        self.assertEqual(pam_status, PamAuthResult.PAM_SUCCESS.value)

    def test_biometric_face_verification_rejection(self):
        """Verify biometric rejection when user is out of range or not present."""
        perception = {
            "user_present": False,
            "distance_cm": 250.0,
            "gaze": "away"
        }
        res = self.auth.verify_user("developer", perception)
        self.assertFalse(res.authenticated)
        self.assertLess(res.confidence_score, 0.88)

    def test_tpm2_enclave_status(self):
        """Verify TPM2 device detection and PCR0+PCR7 binding policy."""
        st = self.enclave.get_enclave_status()
        self.assertIn("tpm2_device", st)
        self.assertIn("PCR0+PCR7", st["pcr_policy"])
        self.assertTrue(st["luks2_auto_unseal"])

    def test_fido2_git_signing_configuration(self):
        """Verify FIDO2 hardware key SSH signing config generation."""
        res = self.enclave.configure_fido2_git_signing("dev@newbianos.org")
        self.assertTrue(res["success"])
        self.assertEqual(res["signing_format"], "ssh-ed25519-sk")
        self.assertEqual(res["git_config"]["commit.gpgsign"], "true")

if __name__ == "__main__":
    unittest.main()
