import subprocess

from axtended_key.models.certificate_paths import CertificatePaths
from axtended_key.utils.logger import logger


class KeychainManager:
    """
    Manages macOS Keychain operations, including importing certificates and configuring trust settings.

    Attributes:
        paths (CertificatePaths): Paths for certificate-related files.
        password (str): Password used to unlock the PKCS#12 certificate file.
    """

    def __init__(self, paths: CertificatePaths, password: str):
        """
        Initialize the KeychainManager.

        Args:
            paths (CertificatePaths): Paths for certificate-related files.
            password (str): Password for unlocking the PKCS#12 file.
        """
        self.paths = paths
        self.password = password

    def import_certificate(self):
        """
        Import a certificate into the macOS login keychain.

        Uses the `security import` command to add the PKCS#12 certificate to the login keychain.

        Raises:
            RuntimeError: If the import process fails.

        See Also:
            https://ss64.com/mac/security-export.html Full reference for `security import` command.
        """
        try:
            logger.log(f"Importing PKCS#12 into the keychain...")

            command_parts = [
                # Command: security import
                ("security", "macOS security tool"),
                ("import", "Import a certificate into the keychain"),
                # Path
                (str(self.paths.p12_file), "Path to the PKCS#12 certificate file"),
                # Password
                ("-P", "Password for the PKCS#12 file"),
                (self.password, "Auto-generated password value"),
                # Trust for codesign
                ("-T", "Specify a trusted app for the certificate"),
                ("/usr/bin/codesign", "Path to the app to trust (codesign)"),
            ]

            command = " ".join(part[0] for part in command_parts)
            subprocess.run(command, check=True, shell=True)
            logger.log("Certificate successfully imported into the keychain.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to import certificate: {e.stderr}")

    def set_trust_for_codesigning(self):
        """
        Configure trust settings for the imported certificate.
        Uses the `security add-trusted-cert` command to mark the certificate as trusted for (only) code signing.

        Raises:
            RuntimeError: If the trust settings process fails.

        See Also:
            https://ss64.com/mac/security-cert.html : Reference for macOS `security add-trusted-cert` command.
        """
        try:
            logger.log(f"Setting trust for certificate at {self.paths.cert_file}...")

            command_parts = [
                # Command: security add-trusted-cert
                ("security", "macOS security tool"),
                ("add-trusted-cert", "Add a trusted certificate"),
                ("-d", "Add to admin cert store (default is user)"),
                ("-r trustRoot", "Specify trust settings for the certificate (e.g., trust root)"),
                ("-p codeSign", "Add trust for code signing"),
                # Path to certificate
                (str(self.paths.cert_file), "Path to the certificate file"),
            ]

            command = " ".join(part[0] for part in command_parts)
            subprocess.run(command, check=True, shell=True)
            logger.log("Trust settings successfully configured for the certificate.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to set trust settings: {e.stderr}")

    def run_all(self):
        """
        Execute all keychain operations in sequence:
        1. Import certificate into default keychain
        2. Set trust for codesign operations

        Raises:
            RuntimeError: If any operation fails.
        """
        logger.log("Starting keychain operations...")
        self.import_certificate()
        self.set_trust_for_codesigning()
        logger.log("Keychain operations completed successfully.")
