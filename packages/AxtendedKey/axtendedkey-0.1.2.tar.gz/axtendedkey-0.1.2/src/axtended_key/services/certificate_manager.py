import subprocess
from axtended_key.models.certificate_metadata import CertificateMetadata
from axtended_key.models.certificate_paths import CertificatePaths


class CertificateManager:
    """Manager for certificate-related operations."""

    def __init__(self, metadata: CertificateMetadata, paths: CertificatePaths):
        self.metadata = metadata
        self.paths = paths

    def generate_openssl_config(self) -> str:
        """Generate the OpenSSL configuration text."""
        return f"""
        [ req ]
        distinguished_name = req_name
        prompt = no
        [ req_name ]
        CN = {self.metadata.common_name}
        [ extensions ]
        basicConstraints=critical,CA:false
        keyUsage=critical,digitalSignature
        extendedKeyUsage=critical,1.3.6.1.5.5.7.3.3
        1.2.840.113635.100.6.1.14=critical,DER:0500
        """.strip()

    def write_openssl_config(self):
        """Write the OpenSSL configuration to a file."""
        with open(self.paths.config_file, "w") as file:
            file.write(self.generate_openssl_config())

    def create_self_signed_certificate(self):
        """Generate a self-signed certificate using OpenSSL."""
        print("Generating self-signed certificate...")
        subprocess.run([
            "openssl", "req", "-newkey", "rsa:2048", "-x509", "-sha256",
            "-days", "365",
            "-keyout", str(self.paths.key_file),
            "-out", str(self.paths.cert_file),
            "-config", str(self.paths.config_file),
            "-passout", f"pass:{self.metadata.password}",
            "-subj", f"/CN={self.metadata.common_name}"
        ], check=True)
        print(f"Certificate generated: {self.paths.cert_file}")

    def package_certificate(self):
        """Package the certificate into PKCS#12 format."""
        print("Packaging certificate into PKCS#12...")
        subprocess.run([
            "openssl", "pkcs12", "-export",
            "-inkey", str(self.paths.key_file),
            "-legacy",
            "-in", str(self.paths.cert_file),
            "-out", str(self.paths.p12_file),
            "-passin", f"pass:{self.metadata.password}",
            "-passout", f"pass:{self.metadata.password}"
        ], check=True)
        print(f"PKCS#12 package created: {self.paths.p12_file}")

    def run_all(self):
        """Run all certificate-related commands in sequence."""
        self.write_openssl_config()
        self.create_self_signed_certificate()
        self.package_certificate()
