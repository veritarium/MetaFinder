"""
MetaFinder - Universal File Metadata Extraction and Filtering System
"""

__version__ = "0.1.0"
__author__ = "MetaFinder Team"

from .scanner import MetadataScanner
from .database import DatabaseManager
from .normalizer import MetadataNormalizer

__all__ = [
    "MetadataScanner",
    "DatabaseManager",
    "MetadataNormalizer",
]
