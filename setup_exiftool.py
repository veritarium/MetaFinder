#!/usr/bin/env python3
"""
ExifTool Setup Script
Automatically downloads and sets up ExifTool for MetaFinder
"""

import sys
import os
import urllib.request
import zipfile
import shutil
from pathlib import Path
import platform


def download_exiftool_windows():
    """Download and setup ExifTool for Windows"""
    print("=" * 60)
    print("📥 ExifTool Setup for Windows")
    print("=" * 60)

    vendor_bin = Path(__file__).parent / 'vendor' / 'bin'
    vendor_bin.mkdir(parents=True, exist_ok=True)

    exiftool_exe = vendor_bin / 'exiftool.exe'

    # Check if already exists
    if exiftool_exe.exists():
        print(f"\n✅ ExifTool already installed at: {exiftool_exe}")
        response = input("\nRedownload anyway? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing version.")
            return True

    print("\n📥 Downloading ExifTool for Windows...")
    print("This may take a minute (~14 MB)...\n")

    # Download URL (update version as needed)
    url = "https://exiftool.org/exiftool-12.70.zip"
    zip_path = vendor_bin / 'exiftool.zip'

    try:
        # Download with progress
        def download_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, (downloaded / total_size) * 100)
            bar_length = 40
            filled = int(bar_length * downloaded / total_size)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f'\r[{bar}] {percent:.1f}%', end='', flush=True)

        urllib.request.urlretrieve(url, zip_path, download_progress)
        print("\n✅ Download complete!")

        # Extract
        print("\n📦 Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(vendor_bin)

        # Find and rename exiftool(-k).exe to exiftool.exe
        exiftool_k = vendor_bin / 'exiftool(-k).exe'
        if exiftool_k.exists():
            exiftool_k.rename(exiftool_exe)
            print(f"✅ ExifTool installed: {exiftool_exe}")
        else:
            print("❌ Could not find exiftool(-k).exe in archive")
            return False

        # Clean up
        zip_path.unlink()
        print("🧹 Cleaned up temporary files")

        print("\n" + "=" * 60)
        print("✅ ExifTool Setup Complete!")
        print("=" * 60)
        print(f"\nExifTool installed at: {exiftool_exe}")
        print("\nYou can now run:")
        print("  python metafinder_gui.py")
        print("  python metafinder_cli.py scan <folder>")

        return True

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("\nManual installation:")
        print("1. Download from: https://exiftool.org/")
        print("2. Extract exiftool(-k).exe")
        print("3. Rename to exiftool.exe")
        print(f"4. Copy to: {vendor_bin}")
        return False


def check_system_exiftool():
    """Check if ExifTool is already installed system-wide"""
    try:
        import subprocess
        result = subprocess.run(
            ['exiftool', '-ver'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ System ExifTool found: version {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False


def main():
    """Main setup function"""
    print("\n" + "=" * 60)
    print("🔧 MetaFinder ExifTool Setup")
    print("=" * 60)

    system_type = platform.system()

    # Check bundled version first
    vendor_bin = Path(__file__).parent / 'vendor' / 'bin'
    if system_type == 'Windows':
        bundled_path = vendor_bin / 'exiftool.exe'
    else:
        bundled_path = vendor_bin / 'exiftool'

    if bundled_path.exists():
        print(f"\n✅ Bundled ExifTool found: {bundled_path}")
        print("\nYou're all set! Run MetaFinder:")
        print("  python metafinder_gui.py")
        return 0

    # Check system installation
    if check_system_exiftool():
        print("\nYou're all set! System ExifTool will be used.")
        print("\nOptionally, you can bundle ExifTool in this project by:")
        if system_type == 'Windows':
            response = input("\nDownload bundled version for portability? (y/N): ")
            if response.lower() == 'y':
                if download_exiftool_windows():
                    return 0
                return 1
        else:
            print(f"  cp $(which exiftool) {vendor_bin}/")
        return 0

    # No ExifTool found - help install
    print("\n⚠️  ExifTool not found!")
    print("\nExifTool is required for MetaFinder to extract file metadata.")

    if system_type == 'Windows':
        print("\n🪟 Windows detected")
        print("\nOption 1: Download bundled version (Recommended)")
        response = input("Download now? (Y/n): ")
        if response.lower() != 'n':
            if download_exiftool_windows():
                return 0
            return 1

        print("\nOption 2: Manual installation")
        print("1. Download from: https://exiftool.org/")
        print("2. Extract and rename exiftool(-k).exe to exiftool.exe")
        print(f"3. Place in: {vendor_bin}")

    elif system_type == 'Darwin':  # macOS
        print("\n🍎 macOS detected")
        print("\nInstall with Homebrew:")
        print("  brew install exiftool")

    else:  # Linux
        print("\n🐧 Linux detected")
        print("\nInstall with package manager:")
        print("  sudo apt install libimage-exiftool-perl    # Debian/Ubuntu")
        print("  sudo dnf install perl-Image-ExifTool       # Fedora")
        print("  sudo pacman -S perl-image-exiftool         # Arch")

    return 1


if __name__ == '__main__':
    sys.exit(main())
