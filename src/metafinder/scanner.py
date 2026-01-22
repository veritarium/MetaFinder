"""
Metadata scanner for MetaFinder
Uses PyExifTool to extract metadata from files
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import subprocess
import sys

try:
    import exiftool
    EXIFTOOL_AVAILABLE = True
except ImportError:
    EXIFTOOL_AVAILABLE = False

from .normalizer import MetadataNormalizer
from .database import DatabaseManager


class MetadataScanner:
    """
    Scans folders and extracts metadata using PyExifTool
    """

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        Initialize scanner

        Args:
            db_manager: Database manager instance (creates default if None)
        """
        if not EXIFTOOL_AVAILABLE:
            raise ImportError(
                "PyExifTool is not installed. "
                "Install it with: pip install pyexiftool\n"
                "Also ensure ExifTool binary is installed: https://exiftool.org/"
            )

        self.db = db_manager or DatabaseManager()
        self.normalizer = MetadataNormalizer()
        self._verify_exiftool()

    def _verify_exiftool(self):
        """Verify ExifTool binary is installed"""
        try:
            result = subprocess.run(
                ['exiftool', '-ver'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = float(result.stdout.strip())
            if version < 12.15:
                print(f"⚠️  Warning: ExifTool {version} is older than recommended (12.15+)")
        except FileNotFoundError:
            raise RuntimeError(
                "ExifTool binary not found. Install from: https://exiftool.org/\n"
                "  - Windows: Download and add to PATH\n"
                "  - macOS: brew install exiftool\n"
                "  - Linux: apt install libimage-exiftool-perl"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("ExifTool check timed out")

    def scan_folder(self,
                   folder_path: str,
                   recursive: bool = True,
                   file_extensions: Optional[List[str]] = None,
                   progress_callback: Optional[Callable[[int, int, str], None]] = None) -> Dict[str, Any]:
        """
        Scan folder and extract metadata from all files

        Args:
            folder_path: Path to folder to scan
            recursive: Scan subdirectories
            file_extensions: List of extensions to include (e.g., ['.jpg', '.pdf'])
            progress_callback: Function(current, total, filename) for progress updates

        Returns:
            Dictionary with scan statistics
        """
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            raise ValueError(f"Invalid folder path: {folder_path}")

        print(f"🔍 Discovering files in {folder_path}...")

        # Discover files
        files = self._discover_files(folder, recursive, file_extensions)
        total_files = len(files)

        if total_files == 0:
            print("❌ No files found to scan")
            return {'scanned': 0, 'failed': 0, 'total': 0}

        print(f"📂 Found {total_files} files")
        print(f"🚀 Starting metadata extraction with PyExifTool...")

        # Process in batches for better performance
        batch_size = 100
        scanned = 0
        failed = 0

        try:
            with exiftool.ExifToolHelper() as et:
                for i in range(0, total_files, batch_size):
                    batch = files[i:i + batch_size]
                    batch_paths = [str(f) for f in batch]

                    try:
                        # Extract metadata for batch (single call!)
                        metadata_list = et.get_metadata(batch_paths)

                        # Process and store each file
                        for j, metadata in enumerate(metadata_list):
                            file_path = batch[j]

                            if progress_callback:
                                progress_callback(scanned + j + 1, total_files, file_path.name)

                            try:
                                # Normalize and store
                                record = self.normalizer.normalize_exiftool_output(metadata)
                                self.db.insert_file(record)
                                scanned += 1
                            except Exception as e:
                                print(f"❌ Error processing {file_path.name}: {e}")
                                failed += 1

                    except Exception as e:
                        print(f"❌ Batch extraction failed: {e}")
                        failed += len(batch)

        except Exception as e:
            print(f"❌ Scanner error: {e}")
            raise

        stats = {
            'scanned': scanned,
            'failed': failed,
            'total': total_files,
            'success_rate': (scanned / total_files * 100) if total_files > 0 else 0
        }

        print(f"\n✅ Scan complete!")
        print(f"   📊 {scanned}/{total_files} files processed ({stats['success_rate']:.1f}% success)")
        if failed > 0:
            print(f"   ⚠️  {failed} files failed")

        return stats

    def scan_single_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Scan a single file and return its metadata

        Args:
            file_path: Path to file

        Returns:
            Normalized file record or None if failed
        """
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            raise ValueError(f"Invalid file path: {file_path}")

        try:
            with exiftool.ExifToolHelper() as et:
                metadata_list = et.get_metadata([str(path)])
                if metadata_list:
                    return self.normalizer.normalize_exiftool_output(metadata_list[0])
        except Exception as e:
            print(f"❌ Error scanning {path.name}: {e}")

        return None

    def _discover_files(self,
                       folder: Path,
                       recursive: bool,
                       file_extensions: Optional[List[str]] = None) -> List[Path]:
        """
        Discover all files in folder

        Args:
            folder: Folder path
            recursive: Scan subdirectories
            file_extensions: Filter by extensions

        Returns:
            List of file paths
        """
        files = []

        if recursive:
            pattern = '**/*'
        else:
            pattern = '*'

        for item in folder.glob(pattern):
            if item.is_file():
                # Filter by extension if specified
                if file_extensions:
                    if item.suffix.lower() in file_extensions:
                        files.append(item)
                else:
                    files.append(item)

        return files

    def rescan_changed_files(self, folder_path: str) -> Dict[str, Any]:
        """
        Rescan only files that have been added or modified since last scan

        Args:
            folder_path: Path to folder

        Returns:
            Scan statistics
        """
        folder = Path(folder_path)
        files = self._discover_files(folder, recursive=True)

        changed_files = []
        for file in files:
            # Check if file exists in database
            existing = self.db.get_file_by_path(str(file.absolute()))

            if not existing:
                # New file
                changed_files.append(file)
            else:
                # Check if modified
                stat = file.stat()
                if stat.st_mtime > existing['modified']:
                    changed_files.append(file)

        if not changed_files:
            print("✅ No changed files found")
            return {'scanned': 0, 'failed': 0, 'total': 0}

        print(f"🔄 Rescanning {len(changed_files)} changed files...")

        # Scan changed files
        return self._scan_file_list(changed_files)

    def _scan_file_list(self, files: List[Path]) -> Dict[str, Any]:
        """Internal method to scan a list of files"""
        total_files = len(files)
        scanned = 0
        failed = 0

        batch_size = 100

        try:
            with exiftool.ExifToolHelper() as et:
                for i in range(0, total_files, batch_size):
                    batch = files[i:i + batch_size]
                    batch_paths = [str(f) for f in batch]

                    try:
                        metadata_list = et.get_metadata(batch_paths)

                        for j, metadata in enumerate(metadata_list):
                            try:
                                record = self.normalizer.normalize_exiftool_output(metadata)
                                self.db.insert_file(record)
                                scanned += 1
                            except Exception as e:
                                print(f"❌ Error: {e}")
                                failed += 1

                    except Exception as e:
                        print(f"❌ Batch failed: {e}")
                        failed += len(batch)

        except Exception as e:
            print(f"❌ Scanner error: {e}")

        return {
            'scanned': scanned,
            'failed': failed,
            'total': total_files,
            'success_rate': (scanned / total_files * 100) if total_files > 0 else 0
        }


def check_requirements() -> Dict[str, bool]:
    """
    Check if all requirements are installed

    Returns:
        Dictionary with requirement status
    """
    status = {}

    # Check PyExifTool
    try:
        import exiftool
        status['pyexiftool'] = True
    except ImportError:
        status['pyexiftool'] = False

    # Check ExifTool binary
    try:
        result = subprocess.run(['exiftool', '-ver'], capture_output=True, timeout=5)
        status['exiftool_binary'] = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        status['exiftool_binary'] = False

    return status
