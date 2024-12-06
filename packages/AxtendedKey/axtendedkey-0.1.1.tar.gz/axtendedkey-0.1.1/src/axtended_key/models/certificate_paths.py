from dataclasses import dataclass
from pathlib import Path


@dataclass
class CertificatePaths:
    """Holds paths for certificate-related files."""
    directory: Path
    config_file: Path
    cert_file: Path
    key_file: Path
    p12_file: Path

    @classmethod
    def from_directory(cls, directory: Path) -> "CertificatePaths":
        """Generate all paths from a base directory."""
        base_name = directory / "AXtendedKey_crt"
        return cls(
            directory=directory,
            config_file=base_name.with_suffix(".conf"),
            cert_file=base_name.with_suffix(".pem"),
            key_file=base_name.with_name(f"{base_name.name}_key.pem"),
            p12_file=base_name.with_suffix(".p12"),
        )
