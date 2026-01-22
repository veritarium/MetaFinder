# MetaFinder Installation Guide

Complete installation guide for all platforms.

## 🎯 Quick Install (All Platforms)

### Step 1: Get the Code

```bash
git clone https://github.com/yourusername/MetaFinder.git
cd MetaFinder
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Setup ExifTool (Automated!)

```bash
python setup_exiftool.py
```

**Done!** The script will automatically:
- ✅ Download ExifTool (Windows)
- ✅ Check system installation (macOS/Linux)
- ✅ Install to `vendor/bin/` (no PATH configuration)
- ✅ Verify it works

## 🪟 Windows Installation

### Automated (Recommended)

```bash
python setup_exiftool.py
```

The script will:
1. Download ExifTool (~14 MB)
2. Extract to `vendor/bin/`
3. Rename to `exiftool.exe`
4. Verify installation

### Manual Installation

If the automated script doesn't work:

1. **Download ExifTool**:
   - Go to: https://exiftool.org/
   - Download: "Windows Executable" (exiftool-12.xx.zip)

2. **Extract and Rename**:
   - Extract the ZIP file
   - Find: `exiftool(-k).exe`
   - Rename to: `exiftool.exe`

3. **Copy to Project**:
   - Copy `exiftool.exe` to `MetaFinder/vendor/bin/`
   - That's it! No PATH needed.

### Verify Installation (Windows)

```bash
python test_prototype.py
```

Should show:
```
✅ Using bundled ExifTool: vendor/bin/exiftool.exe
✅ ExifTool 12.70 ready
```

## 🍎 macOS Installation

### Option 1: System Install (Recommended)

```bash
# Install with Homebrew
brew install exiftool

# Verify
exiftool -ver
```

### Option 2: Bundled (Optional)

```bash
# Run setup script
python setup_exiftool.py

# Or manually copy system version
cp /opt/homebrew/bin/exiftool vendor/bin/
```

### Verify Installation (macOS)

```bash
python test_prototype.py
```

Should show:
```
✅ ExifTool 12.70 ready
```

## 🐧 Linux Installation

### Option 1: System Install (Recommended)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install libimage-exiftool-perl
```

**Fedora:**
```bash
sudo dnf install perl-Image-ExifTool
```

**Arch:**
```bash
sudo pacman -S perl-image-exiftool
```

### Option 2: Bundled (Optional)

```bash
# Copy system version to project
cp /usr/bin/exiftool vendor/bin/
```

### Verify Installation (Linux)

```bash
python test_prototype.py
```

Should show:
```
✅ ExifTool 12.70 ready
```

## 📦 What Gets Installed

### Python Packages

```
PyExifTool>=0.5.6      # Metadata extraction wrapper
customtkinter>=5.2.0   # Modern GUI framework
Pillow>=10.0.0         # Image processing
python-docx>=1.0.0     # Word document parsing
openpyxl>=3.1.0        # Excel parsing
geopy>=2.4.0           # GPS geocoding
tqdm>=4.66.0           # Progress bars
python-dateutil>=2.8.0 # Date parsing
```

### ExifTool Binary

**Bundled Installation** (vendor/bin/):
- Windows: `exiftool.exe` (~14 MB)
- macOS/Linux: `exiftool` (~14 MB)

**System Installation**:
- Windows: Not recommended (PATH configuration)
- macOS: `/opt/homebrew/bin/exiftool` or `/usr/local/bin/exiftool`
- Linux: `/usr/bin/exiftool`

## 🚀 Running MetaFinder

After installation:

### Launch GUI
```bash
python metafinder_gui.py
```

### Use CLI
```bash
# Scan folder
python metafinder_cli.py scan ~/Pictures

# Search files
python metafinder_cli.py search --type image

# View stats
python metafinder_cli.py stats
```

## ✅ Verify Everything Works

```bash
# Run full test suite
python test_prototype.py
```

Expected output:
```
============================================================
🧪 MetaFinder Prototype Test Suite
============================================================
🧪 Testing imports...
  ✅ Core modules imported successfully

🧪 Testing database...
  ✅ Insert successful
  ✅ Retrieval successful
  ✅ Search successful
  ✅ Statistics successful

🧪 Testing normalizer...
  ✅ Normalization successful

🧪 Testing scanner requirements...
  PyExifTool: ✅
  ExifTool binary: ✅

============================================================
Results: 4/4 tests passed (100.0%)
============================================================

🎉 All tests passed! Prototype is working correctly.
```

## 🔧 Troubleshooting

### "PyExifTool not found"

```bash
pip install pyexiftool
```

### "ExifTool binary not found"

**Windows:**
```bash
python setup_exiftool.py
```

**macOS:**
```bash
brew install exiftool
```

**Linux:**
```bash
sudo apt install libimage-exiftool-perl
```

### "Module 'tkinter' not found" (GUI)

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
Already included with Python

**Windows:**
Already included with Python

### "CustomTkinter not found"

```bash
pip install customtkinter
```

### ExifTool version too old

```bash
# Check version
exiftool -ver

# Update (if needed)
# Windows: Download latest from exiftool.org
# macOS: brew upgrade exiftool
# Linux: Update package or download from exiftool.org
```

### GUI doesn't launch

1. **Check Python version**:
   ```bash
   python --version  # Need 3.8+
   ```

2. **Check tkinter**:
   ```bash
   python -c "import tkinter"  # Should have no error
   ```

3. **Check display** (Linux):
   ```bash
   echo $DISPLAY  # Should show :0 or similar
   ```

## 📋 Requirements

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, Linux (any modern distro)
- **Python**: 3.8 or higher
- **RAM**: 500 MB minimum, 1 GB recommended
- **Disk**: 50 MB for app + 5 KB per file indexed

### Python Version Check
```bash
python --version
# or
python3 --version
```

Need 3.8 or higher. If you have an older version:
- **Windows**: Download from python.org
- **macOS**: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11`

## 🎯 Installation Paths

### Where Files Go

```
MetaFinder/
├── vendor/bin/          # Bundled ExifTool (Windows)
│   └── exiftool.exe     # Downloaded by setup_exiftool.py
├── data/                # Database storage
│   └── metafinder.db    # SQLite database (created on first scan)
├── src/metafinder/      # Core library
└── metafinder_gui.py    # Main application
```

### Database Location

Default: `data/metafinder.db`

To use a different location:
```bash
python metafinder_cli.py --database /path/to/custom.db scan ~/Pictures
```

### Bundled vs System ExifTool

MetaFinder checks in this order:
1. **Bundled**: `vendor/bin/exiftool.exe` or `vendor/bin/exiftool`
2. **System**: `exiftool` in PATH

Bundled version takes precedence for consistency and portability.

## 🌟 Benefits of Bundled Approach

### For Windows Users
- ✅ **Zero configuration** - No PATH setup needed
- ✅ **Portable** - Move folder anywhere
- ✅ **Consistent** - Everyone uses same version
- ✅ **Simple** - Just run setup script

### For macOS/Linux Users
- ✅ **System install recommended** - Already in package managers
- ✅ **Optional bundling** - For consistency with team
- ✅ **Automatic fallback** - Uses system if bundled not found

## 📚 Next Steps

After installation:

1. **Test with sample files**:
   ```bash
   python metafinder_cli.py scan data/test-files
   ```

2. **Launch GUI**:
   ```bash
   python metafinder_gui.py
   ```

3. **Scan your files**:
   - Click "Scan Folder"
   - Select a folder
   - Wait for scan to complete
   - Start filtering!

4. **Read documentation**:
   - READY_TO_TEST.md - Testing guide
   - GUI_README.md - GUI features
   - TESTING_GUIDE.md - Test scenarios

## 💡 Tips

### For Developers

- Use virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate     # Windows
  pip install -r requirements.txt
  ```

### For Distribution

- Bundle ExifTool:
  ```bash
  python setup_exiftool.py
  ```

- Package with PyInstaller (future):
  ```bash
  pip install pyinstaller
  pyinstaller --onefile metafinder_gui.py
  ```

## 🆘 Getting Help

If you encounter issues:

1. **Check test results**:
   ```bash
   python test_prototype.py
   ```

2. **Verify ExifTool**:
   ```bash
   exiftool -ver
   ```

3. **Check logs** (if available)

4. **Report issues** with:
   - Error messages
   - System info (OS, Python version)
   - Steps to reproduce

## 🎉 You're Ready!

After following these steps, you should have:
- ✅ Python dependencies installed
- ✅ ExifTool working (bundled or system)
- ✅ All tests passing
- ✅ GUI launching
- ✅ Ready to scan files

**Time to try MetaFinder with your real files!**

See READY_TO_TEST.md for testing guide.
