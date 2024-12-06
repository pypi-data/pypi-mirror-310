from axtended_key.models.certificate_paths import CertificatePaths
import subprocess

class KeychainManager:
    """Manager for handling macOS Keychain operations."""

    def __init__(self, paths: CertificatePaths, password: str):
        """
        Initialize the keychain manager.

        Args:
            paths (CertificatePaths): Paths for certificate-related files.
            password (str): Password for unlocking the PKCS#12 file.
        """
        self.paths = paths
        self.password = password

    def import_certificate(self):
        """
        Import a certificate into the macOS login keychain.

        Raises:
            RuntimeError: If the import process fails.
        """
        try:
            print(f"Importing certificate from {self.paths.p12_file} into the keychain...")
            subprocess.run(
                [
                    "security", "import", str(self.paths.p12_file),
                    "-P", self.password,
                    "-T", "/usr/bin/codesign"
                ],
                check=True
            )
            print("Certificate successfully imported into the keychain.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to import certificate: {e.stderr}")

    def set_trust_for_codesigning(self):
        """
        Set trust settings for the imported certificate.

        Raises:
            RuntimeError: If the trust settings process fails.
        """
        try:
            print(f"Setting trust for certificate at {self.paths.cert_file}...")
            subprocess.run(
                [
                    "security", "add-trusted-cert",
                    "-d", "-r", "trustRoot",
                    "-p", "codeSign", str(self.paths.cert_file)
                ],
                check=True
            )
            print("Trust settings successfully configured for the certificate.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to set trust settings: {e.stderr}")

    def run_all(self):
        """
        Execute all keychain operations: import and set trust.

        Raises:
            RuntimeError: If any operation fails.
        """
        self.import_certificate()
        self.set_trust_for_codesigning()
