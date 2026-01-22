"""
Database layer for MetaFinder
Handles SQLite storage and querying of file metadata
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class DatabaseManager:
    """Manages SQLite database for file metadata storage and querying"""

    def __init__(self, db_path: str = "data/metafinder.db"):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._connect()
        self._create_schema()

    def _connect(self):
        """Establish database connection with optimizations"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

        # SQLite optimizations
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA cache_size=10000")
        self.conn.execute("PRAGMA temp_store=MEMORY")

    def _create_schema(self):
        """Create database tables and indexes"""
        cursor = self.conn.cursor()

        # Main files table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                extension TEXT,
                size INTEGER,
                created REAL,
                modified REAL,
                accessed REAL,

                -- Common indexed fields for fast filtering
                file_type TEXT,
                author TEXT,
                title TEXT,
                date_taken REAL,
                camera_make TEXT,
                camera_model TEXT,

                -- Full metadata as JSON
                metadata TEXT,

                -- Searchable text for FTS
                searchable_text TEXT,

                -- Indexing metadata
                scan_date REAL,
                file_hash TEXT
            )
        """)

        # Full-text search virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS files_fts USING fts5(
                name,
                author,
                title,
                keywords,
                content='files',
                content_rowid='id'
            )
        """)

        # Indexes for common queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_type ON files(file_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_extension ON files(extension)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_size ON files(size)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_modified ON files(modified)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_author ON files(author)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_camera_make ON files(camera_make)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date_taken ON files(date_taken)")

        self.conn.commit()

    def insert_file(self, file_data: Dict[str, Any]) -> int:
        """
        Insert or update file metadata

        Args:
            file_data: Dictionary containing file metadata

        Returns:
            Row ID of inserted/updated file
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO files (
                path, name, extension, size, created, modified, accessed,
                file_type, author, title, date_taken, camera_make, camera_model,
                metadata, searchable_text, scan_date, file_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            file_data.get('path'),
            file_data.get('name'),
            file_data.get('extension'),
            file_data.get('size'),
            file_data.get('created'),
            file_data.get('modified'),
            file_data.get('accessed'),
            file_data.get('file_type'),
            file_data.get('author'),
            file_data.get('title'),
            file_data.get('date_taken'),
            file_data.get('camera_make'),
            file_data.get('camera_model'),
            json.dumps(file_data.get('metadata', {})),
            file_data.get('searchable_text', ''),
            datetime.now().timestamp(),
            file_data.get('file_hash')
        ))

        self.conn.commit()
        return cursor.lastrowid

    def get_file_by_path(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve file metadata by path

        Args:
            path: File path

        Returns:
            Dictionary of file metadata or None
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM files WHERE path = ?", (path,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None

    def search_files(self,
                     file_type: Optional[str] = None,
                     extension: Optional[str] = None,
                     author: Optional[str] = None,
                     camera_make: Optional[str] = None,
                     min_size: Optional[int] = None,
                     max_size: Optional[int] = None,
                     start_date: Optional[float] = None,
                     end_date: Optional[float] = None,
                     text_query: Optional[str] = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search files with filters

        Args:
            file_type: Filter by file type (image, document, audio, etc.)
            extension: Filter by file extension
            author: Filter by author name
            camera_make: Filter by camera manufacturer
            min_size: Minimum file size in bytes
            max_size: Maximum file size in bytes
            start_date: Start date (timestamp)
            end_date: End date (timestamp)
            text_query: Full-text search query
            limit: Maximum results to return

        Returns:
            List of matching file records
        """
        conditions = []
        params = []

        if file_type:
            conditions.append("file_type = ?")
            params.append(file_type)

        if extension:
            conditions.append("extension = ?")
            params.append(extension)

        if author:
            conditions.append("author LIKE ?")
            params.append(f"%{author}%")

        if camera_make:
            conditions.append("camera_make LIKE ?")
            params.append(f"%{camera_make}%")

        if min_size is not None:
            conditions.append("size >= ?")
            params.append(min_size)

        if max_size is not None:
            conditions.append("size <= ?")
            params.append(max_size)

        if start_date:
            conditions.append("modified >= ?")
            params.append(start_date)

        if end_date:
            conditions.append("modified <= ?")
            params.append(end_date)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"""
            SELECT * FROM files
            WHERE {where_clause}
            ORDER BY modified DESC
            LIMIT ?
        """
        params.append(limit)

        cursor = self.conn.cursor()
        cursor.execute(query, params)

        results = []
        for row in cursor.fetchall():
            record = dict(row)
            # Parse JSON metadata
            if record.get('metadata'):
                record['metadata'] = json.loads(record['metadata'])
            results.append(record)

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics

        Returns:
            Dictionary with statistics
        """
        cursor = self.conn.cursor()

        stats = {}

        # Total files
        cursor.execute("SELECT COUNT(*) as count FROM files")
        stats['total_files'] = cursor.fetchone()['count']

        # By file type
        cursor.execute("""
            SELECT file_type, COUNT(*) as count
            FROM files
            WHERE file_type IS NOT NULL
            GROUP BY file_type
        """)
        stats['by_type'] = {row['file_type']: row['count'] for row in cursor.fetchall()}

        # By extension
        cursor.execute("""
            SELECT extension, COUNT(*) as count
            FROM files
            WHERE extension IS NOT NULL
            GROUP BY extension
            ORDER BY count DESC
            LIMIT 20
        """)
        stats['top_extensions'] = {row['extension']: row['count'] for row in cursor.fetchall()}

        # Total size
        cursor.execute("SELECT SUM(size) as total FROM files")
        stats['total_size_bytes'] = cursor.fetchone()['total'] or 0

        # Date range
        cursor.execute("SELECT MIN(modified) as oldest, MAX(modified) as newest FROM files")
        row = cursor.fetchone()
        stats['oldest_file'] = row['oldest']
        stats['newest_file'] = row['newest']

        return stats

    def get_unique_values(self, field: str, limit: int = 100) -> List[str]:
        """
        Get unique values for a field (for filter dropdowns)

        Args:
            field: Field name (author, camera_make, etc.)
            limit: Maximum values to return

        Returns:
            List of unique values
        """
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT DISTINCT {field} as value, COUNT(*) as count
            FROM files
            WHERE {field} IS NOT NULL AND {field} != ''
            GROUP BY {field}
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))

        return [row['value'] for row in cursor.fetchall()]

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
