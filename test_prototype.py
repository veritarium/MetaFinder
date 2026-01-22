#!/usr/bin/env python3
"""
Test script for MetaFinder prototype
Validates that all components work correctly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")

    try:
        from metafinder import MetadataScanner, DatabaseManager, MetadataNormalizer
        print("  ✅ Core modules imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_database():
    """Test database creation and operations"""
    print("\n🧪 Testing database...")

    try:
        from metafinder.database import DatabaseManager

        # Create test database
        db = DatabaseManager("data/test.db")

        # Test insert
        test_record = {
            'path': '/test/file.txt',
            'name': 'file.txt',
            'extension': '.txt',
            'size': 1024,
            'created': 1234567890.0,
            'modified': 1234567890.0,
            'accessed': 1234567890.0,
            'file_type': 'document',
            'author': 'Test Author',
            'title': 'Test File',
            'metadata': {'test': 'data'},
            'searchable_text': 'file.txt Test Author Test File'
        }

        row_id = db.insert_file(test_record)
        print(f"  ✅ Insert successful (row_id: {row_id})")

        # Test retrieval
        retrieved = db.get_file_by_path('/test/file.txt')
        if retrieved:
            print(f"  ✅ Retrieval successful")
        else:
            print(f"  ❌ Retrieval failed")
            return False

        # Test search
        results = db.search_files(file_type='document')
        print(f"  ✅ Search successful ({len(results)} results)")

        # Test stats
        stats = db.get_statistics()
        print(f"  ✅ Statistics successful ({stats['total_files']} files)")

        db.close()
        return True

    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_normalizer():
    """Test metadata normalizer"""
    print("\n🧪 Testing normalizer...")

    try:
        from metafinder.normalizer import MetadataNormalizer

        normalizer = MetadataNormalizer()

        # Test with sample ExifTool output
        sample_exif = {
            'SourceFile': '/test/photo.jpg',
            'FileSize': 1048576,
            'MIMEType': 'image/jpeg',
            'Make': 'Canon',
            'Model': 'EOS 5D Mark IV',
            'DateTimeOriginal': '2024:01:15 14:30:00',
            'Artist': 'John Photographer',
            'Title': 'Test Photo'
        }

        record = normalizer.normalize_exiftool_output(sample_exif)

        # Validate normalized record
        assert record['name'] == 'photo.jpg'
        assert record['extension'] == '.jpg'
        assert record['file_type'] == 'image'
        assert record['camera_make'] == 'Canon'
        assert record['camera_model'] == 'EOS 5D Mark IV'
        assert record['author'] == 'John Photographer'
        assert record['title'] == 'Test Photo'

        print("  ✅ Normalization successful")
        print(f"     - File type: {record['file_type']}")
        print(f"     - Camera: {record['camera_make']} {record['camera_model']}")
        print(f"     - Author: {record['author']}")

        return True

    except Exception as e:
        print(f"  ❌ Normalizer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scanner_requirements():
    """Test scanner requirements (without actually scanning)"""
    print("\n🧪 Testing scanner requirements...")

    try:
        from metafinder.scanner import check_requirements

        reqs = check_requirements()

        print(f"  PyExifTool: {'✅' if reqs['pyexiftool'] else '❌'}")
        print(f"  ExifTool binary: {'✅' if reqs['exiftool_binary'] else '❌'}")

        if not reqs['pyexiftool']:
            print("     Install: pip install pyexiftool")

        if not reqs['exiftool_binary']:
            print("     Install ExifTool from: https://exiftool.org/")
            print("       macOS: brew install exiftool")
            print("       Linux: sudo apt install libimage-exiftool-perl")

        return True

    except Exception as e:
        print(f"  ❌ Scanner test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 MetaFinder Prototype Test Suite")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("Normalizer", test_normalizer),
        ("Scanner Requirements", test_scanner_requirements),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)

    if passed == total:
        print("\n🎉 All tests passed! Prototype is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. See output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
