import subprocess
import sys


def validate_openssl_version():
    try:
        # Run `openssl version` to get the installed version
        result = subprocess.run(["openssl", "version"], stdout=subprocess.PIPE, text=True, check=True)
        version_output = result.stdout.strip()

        # Ensure OpenSSL v3 or higher is installed
        if not version_output.startswith("OpenSSL 3"):
            raise RuntimeError(f"OpenSSL v3 is required. Found: {version_output}")
    except FileNotFoundError:
        raise RuntimeError("OpenSSL is not installed. Please install OpenSSL v3 or higher.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error checking OpenSSL version: {e}")
