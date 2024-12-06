"""Main module."""

import os
import platform
import requests
import zipfile


def download_and_install_font(font_name, font_url, install_dir):
    """
    Download and install a font from the given URL.
    """
    try:
        print(f"Downloading {font_name}...")
        response = requests.get(font_url, stream=True)
        response.raise_for_status()

        # Save ZIP file locally
        zip_path = os.path.join(install_dir, f"{font_name}.zip")
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract ZIP file
        print(f"Extracting {font_name}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)

        # Clean up ZIP file
        os.remove(zip_path)
        print(f"{font_name} installed successfully at {install_dir}!")
    except Exception as e:
        print(f"Failed to install {font_name}: {e}")


def install_fonts():
    """
    Install EB Garamond and Ubuntu Mono fonts.
    """
    fonts = {
        "EB Garamond": "https://fonts.google.com/download?family=EB+Garamond",
        "Ubuntu Mono": "https://fonts.google.com/download?family=Ubuntu+Mono",
    }

    # Determine font installation directory based on OS
    system = platform.system()
    if system == "Linux":
        install_dir = os.path.expanduser("~/.fonts")
    elif system == "Darwin":  # macOS
        install_dir = os.path.expanduser("~/Library/Fonts")
    elif system == "Windows":
        install_dir = os.path.join(os.getenv("APPDATA"), "Fonts")
    else:
        raise OSError("Unsupported operating system")

    os.makedirs(install_dir, exist_ok=True)

    # Download and install each font
    for font_name, font_url in fonts.items():
        download_and_install_font(font_name, font_url, install_dir)


def main():
    print("hello there")
