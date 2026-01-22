# Bundled ExifTool

ExifTool is **pre-installed** in this folder for Windows users!

## ✅ Already Included (Windows)

- ✅ `exiftool.exe` - ExifTool 13.45 launcher (57 KB)
- ✅ `exiftool_files/` - Supporting libraries (34 MB)
- ✅ No download needed - works immediately!

Just clone the repo and run MetaFinder. That's it!

## 🍎 macOS / 🐧 Linux

**Option 1 - Bundle (Optional)**:
- Copy system exiftool here:
  ```bash
  # macOS
  cp /opt/homebrew/bin/exiftool vendor/bin/

  # Linux
  cp /usr/bin/exiftool vendor/bin/
  ```

**Option 2 - System Install (Recommended)**:
```bash
# macOS
brew install exiftool

# Linux
sudo apt install libimage-exiftool-perl
```

MetaFinder checks this folder first, then falls back to system installation.

## 📂 Expected Files

After setup, this folder should contain:

**Windows:**
```
vendor/bin/
└── exiftool.exe
```

**macOS/Linux:**
```
vendor/bin/
└── exiftool
```

## ✅ Verify

Run from MetaFinder root:
```bash
python test_prototype.py
```

Should show:
```
✅ Using bundled ExifTool: vendor/bin/exiftool.exe
✅ ExifTool 12.70 ready
```

## 🎯 Why Bundle?

- ✅ **No installation required** - Just download and run
- ✅ **Consistent version** - Everyone uses same ExifTool
- ✅ **Portable** - Move folder anywhere
- ✅ **Simple** - No PATH configuration needed

## 📝 Notes

- ExifTool is **NOT included in git** (too large, ~14MB)
- Each user downloads their own copy
- Only needed on Windows (macOS/Linux can use system install)
- Falls back to system install if not found here

## 🔗 ExifTool Info

- **Website**: https://exiftool.org/
- **License**: Perl Artistic License / GPL
- **Size**: ~14 MB
- **Version**: 12.70+ recommended

---

**That's it! MetaFinder will work without system-wide installation.**
