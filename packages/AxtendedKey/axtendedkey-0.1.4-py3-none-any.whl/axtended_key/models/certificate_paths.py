from dataclasses import dataclass
from pathlib import Path


@dataclass
class CertificatePaths:
    """
    Represents the paths for certificate-related files, all stored in a temporary directory.

    Attributes:
        directory (Path): Base /tmp directory to store ephemeral certificate files.
        config_file (Path): Configuration file for the certificate. Grants necessary privileges for AX.
        cert_file (Path): Certificate in PEM format.
        key_file (Path): Certificate private key in PEM format.
        p12_file (Path): Certificate in PKCS#12 format.
    """

    directory: Path
    config_file: Path
    cert_file: Path
    key_file: Path
    p12_file: Path

    @classmethod
    def from_directory(cls, directory: Path) -> "CertificatePaths":
        """
        Generate all paths from a base directory.

        Args:
            directory (Path): The base directory for certificate files.

        Returns:
            CertificatePaths: An instance with paths derived from the base directory.

        Raises:
            ValueError: If the directory does not exist.
        """

        base_name = directory / "AXtendedKey_crt"
        return cls(
            directory=directory,
            config_file=base_name.with_suffix(".conf"),
            cert_file=base_name.with_suffix(".pem"),
            key_file=base_name.with_name(f"{base_name.name}_key.pem"),
            p12_file=base_name.with_suffix(".p12"),
        )
