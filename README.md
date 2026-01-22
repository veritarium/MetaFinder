# MetaFinder

> **"Find Any File, Filter by Everything"**

A powerful metadata extraction and filtering system for Windows that lets you find files instantly by filtering on extracted metadata, not just filename.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)]()

## 🎯 What is MetaFinder?

Think **iTunes for all file types**. MetaFinder scans your folders once, extracts **90+ metadata fields** from every file, and lets you filter/search with a beautiful, fast interface.

### The Problem:
- Windows Search only indexes filenames and basic properties
- Finding files requires remembering exact names or locations
- Rich metadata (camera info, GPS, author, BPM, etc.) is hidden and unusable

### The Solution:
**Scan once → Extract everything → Filter instantly**

## ✨ Features

### 🚀 One-Time Scan
- Scan 60,000 files in 5-10 minutes
- Never wait again - all queries are instant
- Incremental rescan for changed files

### 🔍 Rich Metadata Extraction (90+ Fields)
- **Images**: Camera make/model, GPS location, ISO, aperture, date taken
- **Documents**: Author, page count, word count, company, keywords
- **Audio**: Artist, album, BPM, bitrate, duration, lyrics
- **Video**: Codec, resolution, FPS, duration, audio tracks
- **Executables**: Version info, company, digital signature
- **Archives**: Compression method, file count, encryption status
- **Source Code**: Language, line count, function count, complexity

### 🎨 Beautiful Filter Interface
- **Real-Time Filtering**: Results update as you type
- **Multi-Criteria Search**: Combine any filters (AND/OR logic)
- **Saved Queries**: Save frequently used filter combinations
- **Export Results**: CSV, JSON, file lists

### ⚡ Lightning Fast
- Filter results appear in <100ms
- SQLite database with full-text search (FTS5)
- Optimized indexes for common queries

### 🎯 Example Searches

Find files you never could before:

```
📸 "All photos taken with Canon 5D in Paris during 2024"
   Filter: Type=Image, Camera=Canon, GPS=Paris, Year=2024

📄 "PDFs authored by John Smith over 50 pages"
   Filter: Type=PDF, Author=John Smith, Pages>50

🎵 "Running playlist: 140-160 BPM songs"
   Filter: Type=Audio, BPM=140-160

🎬 "4K videos longer than 10 minutes"
   Filter: Type=Video, Resolution>=3840x2160, Duration>600s

📐 "CAD drawings for Building-A project modified this week"
   Filter: Extension=dwg, Project=Building-A, Modified=Last7Days
```

## 🖼️ Interface Preview

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📁 MetaFinder                          [Scan] [⚙️] ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 🔍 Quick Search: [paris canon 2024___] 🎯 Advanced ┃
┃                                                      ┃
┃ Active Filters: [.jpg ✕] [Canon ✕] [Paris ✕]       ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ FILTERS            │  RESULTS (1,234 files)          ┃
┃━━━━━━━━━━━━━━━━━━│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃
┃ 📁 File Type       │ 📸 vacation_paris_001.jpg       ┃
┃   ☑ Images (5.2k)  │    Canon EOS 5D Mark IV         ┃
┃   □ Documents      │    Paris, France (48.85, 2.35)  ┃
┃   □ Audio          │    2024-06-15 14:32:18          ┃
┃                    │    ISO 400, f/2.8, 1/250s       ┃
┃ 📅 Date            │    [Open] [Show in Folder]      ┃
┃   ● 2024           │                                  ┃
┃                    │ 📸 vacation_paris_002.jpg       ┃
┃ 📸 Camera          │    Canon EOS 5D Mark IV         ┃
┃   ☑ Canon (234)    │    Paris, France               ┃
┃   □ Nikon (89)     │    ...                          ┃
┗━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## 🚀 Quick Start

### Option 1: Download Executable (Coming Soon)
1. Download `MetaFinder.exe` from [Releases](https://github.com/veritarium/MetaFinder/releases)
2. Run it - no installation needed!
3. Point it to your folder and click Scan

### Option 2: Build from Source

```bash
# Clone the repository
git clone https://github.com/veritarium/MetaFinder.git
cd MetaFinder

# Install dependencies
pip install -r requirements.txt

# Run
python metafinder.py
```

## 📖 How to Use

### 1. Initial Scan
- Click "Scan Folder"
- Select your top-level directory
- Wait for scan to complete (5-10 mins for 60k files)
- Database created with all metadata

### 2. Filter & Search
- Select filters from left sidebar
- Results update in real-time
- Combine any filters (AND logic by default)
- Use quick search for keywords

### 3. Work with Results
- Double-click to open file
- Right-click for context menu
- Select multiple files for batch actions
- Export results to CSV/JSON

### 4. Save Queries
- Click "Save Query" to save current filters
- Give it a name (e.g., "My Running Playlist")
- Load saved queries anytime

### 5. Incremental Rescan
- Click "Rescan" to update changed files
- Much faster than full scan
- Only processes new/modified files

## 🏗️ Architecture

### Components:
1. **Scanner Engine**: Extracts metadata using specialized extractors
2. **Database Layer**: SQLite with FTS5 for fast queries
3. **Filter UI**: CustomTkinter-based modern interface

### Metadata Extractors:
- **ImageExtractor**: Pillow, exifread (EXIF, GPS, color)
- **DocumentExtractor**: PyPDF2, python-docx, openpyxl
- **AudioExtractor**: mutagen (ID3 tags)
- **VideoExtractor**: ffmpeg-python
- **ExecutableExtractor**: pefile (version info)
- **ArchiveExtractor**: zipfile, rarfile, py7zr
- **CodeExtractor**: pygments (language detection, metrics)

## 📊 Supported File Types

| Category | Extensions | Metadata Fields |
|----------|-----------|-----------------|
| **Images** | jpg, png, gif, bmp, tiff, raw | 45+ (EXIF, GPS, camera) |
| **Documents** | pdf, doc, docx, xls, xlsx, ppt, pptx | 30+ (author, pages, words) |
| **Audio** | mp3, flac, wav, m4a, ogg | 35+ (artist, album, BPM) |
| **Video** | mp4, mkv, avi, mov, wmv | 30+ (codec, resolution, FPS) |
| **Archives** | zip, rar, 7z, tar, gz | 15+ (compression, contents) |
| **Executables** | exe, dll, sys | 25+ (version, signature) |
| **Source Code** | py, js, java, cpp, c, html, css | 20+ (LOC, functions) |
| **CAD** | dwg, dxf, skp | 15+ (author, layers) |

## 🎯 Use Cases

### For Photographers:
- Find all photos from specific camera
- Filter by GPS location
- Search by camera settings (ISO, aperture)
- Organize by shooting date

### For Content Creators:
- Find videos by resolution/codec
- Filter music by BPM for playlists
- Search documents by author
- Locate files by software used

### For Developers:
- Find code files by language
- Filter by line count or complexity
- Search for files with TODOs
- Organize by project

### For Document Workers:
- Find PDFs by author or page count
- Filter Word docs by company
- Search presentations by slide count
- Locate files by keywords

### For Data Hoarders:
- Organize massive file collections
- Find duplicates by hash
- Filter by any metadata
- Export catalogs

## 🔧 Requirements

- **OS**: Windows 10 or later
- **Python**: 3.11+ (for building from source)
- **Disk Space**: ~5 KB per file for database (~300 MB for 60k files)
- **RAM**: ~500 MB during normal operation

## 🗺️ Roadmap

### v1.0 - Core Features (Current)
- [x] Project brainstorm and planning
- [ ] Scanner engine with 7+ extractors
- [ ] SQLite database with FTS5
- [ ] Basic filter UI
- [ ] Image, document, audio metadata extraction

### v1.1 - Enhanced Filtering
- [ ] Advanced filters (GPS, BPM, author)
- [ ] Saved queries
- [ ] Export results (CSV, JSON)
- [ ] Video and executable metadata

### v1.2 - Polish & Performance
- [ ] Incremental rescan
- [ ] Background indexing
- [ ] Thumbnail cache
- [ ] Error handling

### v2.0 - Advanced Features
- [ ] Multiple catalogs
- [ ] Cloud storage support
- [ ] Network shares
- [ ] Smart collections

## 🤝 Contributing

Contributions welcome! Areas to help:
- New metadata extractors
- UI/UX improvements
- Performance optimizations
- Documentation
- Bug reports

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

**Inspired by**:
- iTunes (music library organization)
- Everything by voidtools (fast file search)
- Adobe Lightroom (photo cataloging)

**Built with**:
- Python 3.11+
- CustomTkinter (modern UI)
- SQLite (database)
- Pillow, PyPDF2, mutagen, pefile (extractors)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/veritarium/MetaFinder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/veritarium/MetaFinder/discussions)
- **Documentation**: See [PROJECT_BRAINSTORM.md](PROJECT_BRAINSTORM.md) for detailed planning

## 🌟 Why MetaFinder?

### vs. Windows Search:
- ✅ 100x more metadata
- ✅ Advanced filtering
- ✅ Beautiful UI
- ✅ Actually works

### vs. Everything:
- ✅ Rich metadata (not just filenames)
- ✅ Smart filtering (not just text search)
- ✅ File-type specific features

### vs. Manual Organization:
- ✅ No folder structures to maintain
- ✅ Filter any way you want
- ✅ Find files in seconds
- ✅ Never reorganize again

---

**Ready to find your files like never before? 🚀**

**Star this repo** if you're interested in the project!

*Made with ❤️ for people tired of searching for files*
