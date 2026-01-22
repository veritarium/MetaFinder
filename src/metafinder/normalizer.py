"""
Metadata normalizer for MetaFinder
Converts ExifTool output into our standardized database schema
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import mimetypes


class MetadataNormalizer:
    """Normalizes metadata from various sources into our schema"""

    # Map file types based on MIME types
    FILE_TYPE_MAP = {
        'image': ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/tiff', 'image/webp'],
        'document': ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'],
        'audio': ['audio/mpeg', 'audio/mp4', 'audio/x-wav', 'audio/flac', 'audio/ogg'],
        'video': ['video/mp4', 'video/x-msvideo', 'video/x-matroska', 'video/quicktime', 'video/x-ms-wmv'],
        'archive': ['application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed', 'application/x-tar'],
        'executable': ['application/x-msdownload', 'application/x-executable'],
    }

    def __init__(self):
        """Initialize normalizer"""
        pass

    def normalize_exiftool_output(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert ExifTool output to our database schema

        Args:
            exif_data: Raw output from ExifTool

        Returns:
            Normalized file record
        """
        file_path = exif_data.get('SourceFile', '')
        path_obj = Path(file_path)

        # Basic file info
        record = {
            'path': str(path_obj.absolute()),
            'name': path_obj.name,
            'extension': path_obj.suffix.lower(),
        }

        # File system metadata
        try:
            stat = path_obj.stat()
            record['size'] = stat.st_size
            record['created'] = stat.st_ctime
            record['modified'] = stat.st_mtime
            record['accessed'] = stat.st_atime
        except (OSError, FileNotFoundError):
            record['size'] = exif_data.get('FileSize', 0)
            record['created'] = None
            record['modified'] = None
            record['accessed'] = None

        # Determine file type
        record['file_type'] = self._determine_file_type(exif_data, path_obj)

        # Extract common fields based on file type
        if record['file_type'] == 'image':
            record.update(self._extract_image_metadata(exif_data))
        elif record['file_type'] == 'document':
            record.update(self._extract_document_metadata(exif_data))
        elif record['file_type'] == 'audio':
            record.update(self._extract_audio_metadata(exif_data))
        elif record['file_type'] == 'video':
            record.update(self._extract_video_metadata(exif_data))

        # Store full metadata as JSON
        record['metadata'] = self._clean_metadata(exif_data)

        # Build searchable text
        record['searchable_text'] = self._build_searchable_text(record)

        # File hash (optional, for duplicate detection)
        record['file_hash'] = None  # Can add later if needed

        return record

    def _determine_file_type(self, exif_data: Dict[str, Any], path_obj: Path) -> str:
        """
        Determine file type from metadata and extension

        Args:
            exif_data: ExifTool output
            path_obj: Path object

        Returns:
            File type string
        """
        # Try MIME type first
        mime_type = exif_data.get('MIMEType') or exif_data.get('File:MIMEType')
        if mime_type:
            for file_type, mime_list in self.FILE_TYPE_MAP.items():
                if mime_type in mime_list:
                    return file_type

        # Fallback to extension-based detection
        ext = path_obj.suffix.lower()
        extension_map = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.raw', '.cr2', '.nef'],
            'document': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf'],
            'audio': ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'archive': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'executable': ['.exe', '.dll', '.so', '.dylib'],
            'code': ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs'],
        }

        for file_type, extensions in extension_map.items():
            if ext in extensions:
                return file_type

        return 'unknown'

    def _extract_image_metadata(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract image-specific metadata"""
        data = {}

        # Camera info
        data['camera_make'] = exif_data.get('Make') or exif_data.get('EXIF:Make')
        data['camera_model'] = exif_data.get('Model') or exif_data.get('EXIF:Model')

        # Date taken
        date_str = (exif_data.get('DateTimeOriginal') or
                   exif_data.get('CreateDate') or
                   exif_data.get('EXIF:DateTimeOriginal'))
        if date_str:
            data['date_taken'] = self._parse_exif_date(date_str)

        # Author/Artist
        data['author'] = exif_data.get('Artist') or exif_data.get('Creator') or exif_data.get('EXIF:Artist')

        # Title
        data['title'] = exif_data.get('Title') or exif_data.get('XMP:Title')

        return data

    def _extract_document_metadata(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract document-specific metadata"""
        data = {}

        # Author
        data['author'] = (exif_data.get('Author') or
                         exif_data.get('Creator') or
                         exif_data.get('PDF:Author') or
                         exif_data.get('XMP:Creator'))

        # Title
        data['title'] = (exif_data.get('Title') or
                        exif_data.get('PDF:Title') or
                        exif_data.get('XMP:Title'))

        # Creation date
        date_str = (exif_data.get('CreateDate') or
                   exif_data.get('CreationDate') or
                   exif_data.get('PDF:CreateDate'))
        if date_str:
            data['date_taken'] = self._parse_exif_date(date_str)

        return data

    def _extract_audio_metadata(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract audio-specific metadata"""
        data = {}

        # Artist
        data['author'] = (exif_data.get('Artist') or
                         exif_data.get('ID3:Artist') or
                         exif_data.get('Vorbis:Artist'))

        # Title
        data['title'] = (exif_data.get('Title') or
                        exif_data.get('ID3:Title') or
                        exif_data.get('Vorbis:Title'))

        return data

    def _extract_video_metadata(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract video-specific metadata"""
        data = {}

        # Creation date
        date_str = (exif_data.get('CreateDate') or
                   exif_data.get('CreationDate') or
                   exif_data.get('QuickTime:CreateDate'))
        if date_str:
            data['date_taken'] = self._parse_exif_date(date_str)

        # Title
        data['title'] = exif_data.get('Title') or exif_data.get('QuickTime:Title')

        return data

    def _parse_exif_date(self, date_str: str) -> Optional[float]:
        """
        Parse EXIF date string to timestamp

        Args:
            date_str: Date string from EXIF

        Returns:
            Unix timestamp or None
        """
        if not date_str:
            return None

        # Common EXIF date formats
        formats = [
            '%Y:%m:%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%Y:%m:%d %H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str[:19], fmt[:19])
                return dt.timestamp()
            except (ValueError, TypeError):
                continue

        return None

    def _clean_metadata(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and organize metadata for JSON storage

        Args:
            exif_data: Raw ExifTool output

        Returns:
            Cleaned metadata dictionary
        """
        # Remove binary data and very large fields
        cleaned = {}
        for key, value in exif_data.items():
            # Skip binary data
            if isinstance(value, bytes):
                continue
            # Skip very large strings (like embedded thumbnails)
            if isinstance(value, str) and len(value) > 10000:
                continue
            # Skip internal ExifTool fields
            if key.startswith('System:'):
                continue

            cleaned[key] = value

        return cleaned

    def _build_searchable_text(self, record: Dict[str, Any]) -> str:
        """
        Build searchable text from record fields

        Args:
            record: File record

        Returns:
            Combined searchable text
        """
        parts = [
            record.get('name', ''),
            record.get('author', ''),
            record.get('title', ''),
            record.get('camera_make', ''),
            record.get('camera_model', ''),
        ]

        # Add metadata values
        metadata = record.get('metadata', {})
        if metadata:
            # Add keywords, tags, description, etc.
            for key in ['Keywords', 'Tags', 'Description', 'Comment', 'Subject']:
                if key in metadata:
                    parts.append(str(metadata[key]))

        return ' '.join(filter(None, parts))

    def calculate_file_hash(self, file_path: str, algorithm: str = 'md5') -> Optional[str]:
        """
        Calculate file hash for duplicate detection

        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256)

        Returns:
            Hex digest of file hash
        """
        try:
            hash_func = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except (OSError, FileNotFoundError):
            return None
