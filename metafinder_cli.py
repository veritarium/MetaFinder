#!/usr/bin/env python3
"""
MetaFinder CLI Demo
Command-line interface for scanning and searching file metadata
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from metafinder import MetadataScanner, DatabaseManager
from metafinder.scanner import check_requirements


def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def format_timestamp(timestamp: float) -> str:
    """Format timestamp to readable date"""
    if not timestamp:
        return "Unknown"
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def print_file_record(record: dict, verbose: bool = False):
    """Print a file record in a nice format"""
    print(f"\n📄 {record['name']}")
    print(f"   Path: {record['path']}")
    print(f"   Type: {record['file_type']} ({record['extension']})")
    print(f"   Size: {format_size(record['size'] or 0)}")
    print(f"   Modified: {format_timestamp(record['modified'])}")

    if record.get('author'):
        print(f"   Author: {record['author']}")
    if record.get('title'):
        print(f"   Title: {record['title']}")
    if record.get('camera_make'):
        print(f"   Camera: {record['camera_make']} {record.get('camera_model', '')}")
    if record.get('date_taken'):
        print(f"   Taken: {format_timestamp(record['date_taken'])}")

    if verbose and record.get('metadata'):
        print("\n   📊 Full Metadata:")
        metadata = record['metadata']
        for key, value in list(metadata.items())[:20]:  # Show first 20 fields
            if isinstance(value, (str, int, float)):
                print(f"      {key}: {value}")


def cmd_scan(args):
    """Scan a folder"""
    print("=" * 60)
    print("🔍 MetaFinder - Folder Scanner")
    print("=" * 60)

    # Check requirements
    print("\n📋 Checking requirements...")
    reqs = check_requirements()

    if not reqs['pyexiftool']:
        print("❌ PyExifTool not installed")
        print("   Install: pip install pyexiftool")
        return 1

    if not reqs['exiftool_binary']:
        print("❌ ExifTool binary not found")
        print("   Install from: https://exiftool.org/")
        return 1

    print("✅ All requirements satisfied")

    # Initialize scanner
    db = DatabaseManager(args.database)
    scanner = MetadataScanner(db)

    # Progress callback
    def progress(current, total, filename):
        percent = (current / total) * 100
        print(f"\r   [{current}/{total}] {percent:.1f}% - {filename[:50]:<50}", end='')

    # Scan folder
    stats = scanner.scan_folder(
        args.folder,
        recursive=not args.no_recursive,
        progress_callback=progress
    )

    print("\n\n" + "=" * 60)
    print("📊 Scan Statistics")
    print("=" * 60)
    print(f"Total files: {stats['total']}")
    print(f"Successfully scanned: {stats['scanned']}")
    print(f"Failed: {stats['failed']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")

    return 0


def cmd_search(args):
    """Search files"""
    print("=" * 60)
    print("🔎 MetaFinder - File Search")
    print("=" * 60)

    db = DatabaseManager(args.database)

    # Build search parameters
    search_params = {
        'limit': args.limit
    }

    if args.type:
        search_params['file_type'] = args.type
    if args.extension:
        search_params['extension'] = args.extension
    if args.author:
        search_params['author'] = args.author
    if args.camera:
        search_params['camera_make'] = args.camera
    if args.min_size:
        search_params['min_size'] = args.min_size
    if args.max_size:
        search_params['max_size'] = args.max_size

    # Search
    results = db.search_files(**search_params)

    print(f"\n✅ Found {len(results)} files")

    if results:
        for record in results:
            print_file_record(record, verbose=args.verbose)

    return 0


def cmd_stats(args):
    """Show database statistics"""
    print("=" * 60)
    print("📊 MetaFinder - Database Statistics")
    print("=" * 60)

    db = DatabaseManager(args.database)
    stats = db.get_statistics()

    print(f"\n📁 Total Files: {stats['total_files']}")
    print(f"💾 Total Size: {format_size(stats['total_size_bytes'])}")

    if stats['oldest_file']:
        print(f"📅 Date Range: {format_timestamp(stats['oldest_file'])} to {format_timestamp(stats['newest_file'])}")

    print("\n📂 Files by Type:")
    for file_type, count in stats['by_type'].items():
        print(f"   {file_type}: {count}")

    print("\n📝 Top Extensions:")
    for ext, count in list(stats['top_extensions'].items())[:10]:
        print(f"   {ext}: {count}")

    return 0


def cmd_info(args):
    """Show info about a specific file"""
    print("=" * 60)
    print("ℹ️  MetaFinder - File Info")
    print("=" * 60)

    db = DatabaseManager(args.database)
    scanner = MetadataScanner(db)

    # Get file info
    path = Path(args.file).absolute()
    if not path.exists():
        print(f"❌ File not found: {args.file}")
        return 1

    # Check if already in database
    record = db.get_file_by_path(str(path))

    if not record or args.rescan:
        print("\n🔍 Scanning file...")
        record = scanner.scan_single_file(str(path))

        if record:
            db.insert_file(record)
            print("✅ File scanned and saved to database")
        else:
            print("❌ Failed to scan file")
            return 1
    else:
        print("\n✅ File found in database")

    print_file_record(record, verbose=True)

    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='MetaFinder - Universal File Metadata Extraction and Search',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a folder
  %(prog)s scan ~/Pictures

  # Search for Canon photos
  %(prog)s search --type image --camera Canon

  # Search for PDFs by author
  %(prog)s search --type document --extension .pdf --author "John Smith"

  # Show database statistics
  %(prog)s stats

  # Get info about a specific file
  %(prog)s info ~/Pictures/photo.jpg
        """
    )

    parser.add_argument(
        '--database', '-d',
        default='data/metafinder.db',
        help='Database path (default: data/metafinder.db)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan a folder for files')
    scan_parser.add_argument('folder', help='Folder to scan')
    scan_parser.add_argument('--no-recursive', action='store_true', help='Do not scan subdirectories')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for files')
    search_parser.add_argument('--type', '-t', help='File type (image, document, audio, video)')
    search_parser.add_argument('--extension', '-e', help='File extension (e.g., .jpg, .pdf)')
    search_parser.add_argument('--author', '-a', help='Author/creator name')
    search_parser.add_argument('--camera', '-c', help='Camera make')
    search_parser.add_argument('--min-size', type=int, help='Minimum file size in bytes')
    search_parser.add_argument('--max-size', type=int, help='Maximum file size in bytes')
    search_parser.add_argument('--limit', '-l', type=int, default=100, help='Maximum results (default: 100)')
    search_parser.add_argument('--verbose', '-v', action='store_true', help='Show full metadata')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show info about a specific file')
    info_parser.add_argument('file', help='File path')
    info_parser.add_argument('--rescan', action='store_true', help='Rescan file even if in database')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to command
    commands = {
        'scan': cmd_scan,
        'search': cmd_search,
        'stats': cmd_stats,
        'info': cmd_info,
    }

    try:
        return commands[args.command](args)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
