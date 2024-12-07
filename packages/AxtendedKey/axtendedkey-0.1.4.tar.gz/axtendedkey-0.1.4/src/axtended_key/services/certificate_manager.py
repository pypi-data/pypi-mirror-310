import shlex
import subprocess

from axtended_key.models.certificate_metadata import CertificateMetadata
from axtended_key.models.certificate_paths import CertificatePaths
from axtended_key.utils.logger import logger


class CertificateManager:
    """
    Manages operations related to certificates, including generating OpenSSL configurations,
    creating self-signed certificates, and packaging them into PKCS#12 format.

    Attributes:
        metadata (CertificateMetadata): Metadata for the certificate, including the common name and password.
        paths (CertificatePaths): Paths for certificate-related files.
    """

    def __init__(self, metadata: CertificateMetadata, paths: CertificatePaths):
        """
        Initializes the CertificateManager.

        Args:
            metadata (CertificateMetadata): Metadata for the certificate.
            paths (CertificatePaths): Paths for certificate-related files.
        """
        self.metadata = metadata
        self.paths = paths

    def generate_openssl_config(self) -> str:
        """
        Generate the OpenSSL configuration file.

        A default X.509 self-signed certificate is not compatible with the macOS requirements for AX permissions.
        This (correct) configuration is built at run-time, and attached to the self-signed certificate.

        Returns:
            str: The OpenSSL configuration text.

        See Also:
            https://docs.openssl.org/master/man5/x509v3_config: Config file format

        Verbose Explanation:
        [ req ] Configuration
            Controls how OpenSSL generates Certificate Signing Requests (CSRs) and self-signed certificates.
            By default, the user would be prompted for both actions.

            The below configuration is used to instead:
            1. Not prompt for either action
            2. Use a common Distinguished Name (DN) and Common Name (CN)

            Without this modification, macOS would not recognize the generated certificate as valid for AX permissions.

            See: https://docs.openssl.org/master/man1/openssl-req/#examples

        [ req_name ] Configuration
            Controls configuration for distinguished name (DN) fields.

            The only required change is to set the common name (CN). Doing so:
            1. Allows macOS to identify the certificate and link it to the correct app requesting it (codesign).
            2. Makes the certificate easily found, and removed or otherwise managed, via Keychain.

        [ extensions ] Configuration
            Controls additional information, behavior, and constraints for the generated certificate.

            Required changes are documented below.

            Basic Constraints: Is this a certificate authority?
            ```
            basicConstraints: critical,CA:false
            Marks this certificate as not being a certificate authority (CA).
            ```

            Key Usage: What can this be used for?
            ```
            keyUsage: critical,digitalSignature
            Defines the permitted usages of the key.
            This certificate only requires digital signature: allows signing of content to assure authenticity.
            ```

            Extended Key Usage: What advanced things can this be used for?
            ```
            extendedKeyUsage: critical,1.3.6.1.5.5.7.3.3
            1.2.840.113635.100.6.1.14 = critical,DER:0500
            ```
            Permits usage of two specific Object Identifiers (OIDs).
            An OID is a universally-unique ID that maps to a specific purpose, governed by committee.

            Let's break down 1.3.6.1.5.5.7.3.3:
            1: Who assigned this ID?
               International Organization for Standardization (ISO)
            3: Which organization was assigned?
               Frank Farance (Key participant in ISO organization; registered 1987)
            6: Which sub-classification of an organization was assigned?
               Department of Defense (Registered in 1988)
            1: Which category is this OID?
               Internet (Registered in 1988)
            5: Which subcategory is this OID?
               Security
            5: Which subcategory is this OID?
               Security mechanisms
            7: Which subcategory is this OID?
               Public-Key Infrastructure (X.509)
            3: Which subcategory is this OID?
               Extended Key Purposes
            3: What is this final OID?
               Signing of downloadable executable code

            Likewise, the second OID of `1.2.840.113635.100.6.1.14` maps to `Apple Custom Extension "devid_install"`:
            https://www.apple.com/certificateauthority/pdf/Apple_Developer_ID_CPS_v1.1.pdf

            This is all to say that this configuration is necessary to declare the self-signed certificate to:
            1. Sign executable code, ensuring integrity and authenticity.
            2. Sign a macOS application distributed outside the Mac App Store.

            This Package Name
            By now you should understand the package name:
            AX = Accessibility (permissions to enable for codesign)
            Extended Key Usage = Adds additional purposes (like code signing) for the certificate's purpose.
            AXtendedKey = Builds a certificate to allow extended key usage in AX-related codesign capability.
        """
        config_parts = [
            # [ req ] Configuration
            ("[ req ]", "Main configuration section for OpenSSL request"),
            ("distinguished_name = req_name", "Specifies the distinguished name section"),
            ("prompt = no", "Disables prompts for distinguished name fields"),
            # [ req_name ] Configuration
            ("[ req_name ]", "Defines the distinguished name fields"),
            (f"CN = {self.metadata.common_name}", "Sets the Common Name field"),
            # [ extensions ] Configuration
            ("[ extensions ]", "Specifies certificate extensions"),
            ("basicConstraints = critical,CA:false", "Marks the certificate as non-CA"),
            ("keyUsage = critical,digitalSignature", "Specifies key usage (e.g., digital signature)"),
            ("extendedKeyUsage = critical,1.3.6.1.5.5.7.3.3", "Allows the certificate for code signing"),
            ("1.2.840.113635.100.6.1.14 = critical,DER:0500", "Apple-specific extension for AX permissions"),
        ]

        config_lines = [part[0] for part in config_parts]
        return "\n".join(config_lines)

    def write_openssl_config(self):
        """
        Write the OpenSSL configuration to the specified file path.

        Raises:
            OSError: If writing the file fails.
        """
        logger.log(f"Writing OpenSSL configuration to {self.paths.config_file}...")
        with open(self.paths.config_file, "w") as file:
            file.write(self.generate_openssl_config())
            logger.log("OpenSSL configuration file written successfully.")

    def create_self_signed_certificate(self):
        """
        Generate a self-signed certificate using OpenSSL.

        Raises:
            subprocess.CalledProcessError: If the OpenSSL command fails.

        See Also:
            https://docs.openssl.org/master/man1/openssl-req/: Certificate request documentation
        """
        logger.log("Generating self-signed certificate...")

        command_parts = [
            # Command: openssl req
            ("openssl req", "OpenSSL certificate request tool"),
            ("-newkey rsa:2048", "Generate a new 2048-bit RSA key pair"),
            ("-x509", "Create a self-signed certificate"),
            ("-sha256", "Use SHA-256 for the signature algorithm"),
            ("-days 365", "Set the certificate to expire in 365 days"),
            # Certificate paths
            (f"-keyout {shlex.quote(str(self.paths.key_file))}", "Path to save the private key file"),
            (f"-out {shlex.quote(str(self.paths.cert_file))}", "Path to save the self-signed certificate"),
            (f"-config {shlex.quote(str(self.paths.config_file))}", "Path to the OpenSSL configuration file"),
            # Password and subject
            (f"-passout pass:{shlex.quote(str(self.metadata.password))}", "Password for encrypting the private key"),
            (f"-subj /CN={shlex.quote(str(self.metadata.common_name))}", "Subject with the certificate's common name"),
        ]

        command = " ".join(part[0] for part in command_parts)
        subprocess.run(command, check=True, shell=True)

        logger.log(f"Certificate generated: {self.paths.cert_file}")

    def package_certificate(self):
        """
        Package the generated certificate and key into PKCS#12 format.

        Raises:
            subprocess.CalledProcessError: If the OpenSSL command fails.

        See Also:
            https://docs.openssl.org/master/man1/openssl-pkcs12/: Docs for pkcs12 command
        """
        logger.log("Packaging certificate into PKCS#12...")

        command_parts = [
            # Command: openssl pkcs12
            ("openssl pkcs12", "OpenSSL PKCS#12 tool"),
            ("-export", "Create the PKCS#12 file instead of only parsing"),
            ("-legacy", "Necessary to ensure cipher compatibility with macOS"),
            # Certificate paths
            (f"-inkey {shlex.quote(str(self.paths.key_file))}", "Path to the private key file"),
            (f"-in {shlex.quote(str(self.paths.cert_file))}", "Path to the PEM certificate file"),
            (f"-out {shlex.quote(str(self.paths.p12_file))}", "Path to the output PKCS#12 file"),
            # Passwords
            (f"-passin pass:{shlex.quote(str(self.metadata.password))}", "Input password for the private key"),
            (f"-passout pass:{shlex.quote(str(self.metadata.password))}", "Output password for the PKCS#12 file"),
        ]

        command = " ".join(part[0] for part in command_parts)
        subprocess.run(command, check=True, shell=True)
        logger.log(f"PKCS#12 package created: {self.paths.p12_file}")

    def run_all(self):
        """
        Execute the full sequence of certificate-related commands:
        1. Generate the OpenSSL configuration.
        2. Create a self-signed certificate.
        3. Package the certificate into PKCS#12 format.

        Raises:
            Exception: If any step fails.
        """
        logger.log("Starting full certificate generation process...")
        self.write_openssl_config()
        self.create_self_signed_certificate()
        self.package_certificate()
        logger.log("Certificate generation process completed successfully.")
