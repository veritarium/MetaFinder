#!/usr/bin/env python3
"""
Test GUI components without requiring display
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_gui_imports():
    """Test that GUI can be imported"""
    print("🧪 Testing GUI imports...")

    try:
        import customtkinter
        print("  ✅ CustomTkinter available")
    except ImportError:
        print("  ❌ CustomTkinter not installed")
        return False

    try:
        # Import the GUI module (but don't instantiate)
        import metafinder_gui
        print("  ✅ GUI module imports successfully")
    except ImportError as e:
        print(f"  ❌ GUI import failed: {e}")
        return False
    except Exception as e:
        # Some exceptions are OK (like display not available)
        if "DISPLAY" in str(e) or "Tcl" in str(e):
            print("  ✅ GUI module loads (no display available, but code is valid)")
        else:
            print(f"  ❌ GUI error: {e}")
            return False

    return True


def test_gui_structure():
    """Test that GUI class structure is correct"""
    print("\n🧪 Testing GUI structure...")

    try:
        # Import without instantiating
        import metafinder_gui

        # Check class exists
        assert hasattr(metafinder_gui, 'MetaFinderGUI')
        print("  ✅ MetaFinderGUI class exists")

        # Check main function exists
        assert hasattr(metafinder_gui, 'main')
        print("  ✅ main() function exists")

        return True

    except Exception as e:
        print(f"  ❌ Structure test failed: {e}")
        return False


def main():
    """Run GUI tests"""
    print("=" * 60)
    print("🧪 MetaFinder GUI Test Suite")
    print("=" * 60)

    tests = [
        ("GUI Imports", test_gui_imports),
        ("GUI Structure", test_gui_structure),
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
    print("📊 Test Results")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 GUI is ready! Run with: python3 metafinder_gui.py")
        print("\nNote: GUI requires a display to run. Tests verify code structure only.")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
