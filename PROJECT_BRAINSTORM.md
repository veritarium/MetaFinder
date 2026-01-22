# MetaFinder - Project Brainstorm & Planning

## 🎯 Core Concept

**"iTunes for All File Types"** - A powerful metadata extraction and filtering system that lets you find any file instantly by filtering on extracted metadata, not just filename.

## 💡 The Problem We're Solving

### Current Pain Points:
1. **Windows Search is Limited**: Only searches filenames and basic properties
2. **Manual Organization is Tedious**: Creating folder structures takes forever
3. **Metadata is Hidden**: Files have rich metadata but no way to use it
4. **Can't Answer Questions Like**:
   - "Show me all photos taken with my Canon camera in Paris"
   - "Find all PDFs authored by John that are over 50 pages"
   - "Show me music with 140-160 BPM for my running playlist"
   - "Find CAD drawings modified in the last week"
   - "Which files did I download from email?"

### Our Solution:
**Scan once → Extract everything → Filter instantly**

## 🎨 User Experience Vision

### Workflow:
```
1. User Points to Folder
   ↓
2. Scan Extracts ALL Metadata (5 mins for 60k files)
   ↓
3. Database Created (rich SQLite catalog)
   ↓
4. Beautiful Filter Interface Opens
   ↓
5. User Applies Filters in Real-Time
   ↓
6. Results Show Instantly
   ↓
7. Double-Click Opens File
```

### Key Principles:
- ✅ **One-Time Scan**: Never wait again after initial scan
- ✅ **No AI**: Pure metadata extraction (fast, reliable, offline)
- ✅ **Tag-Based**: Everything becomes a filterable tag
- ✅ **Instant Results**: Database queries are milliseconds
- ✅ **Non-Destructive**: Original files untouched
- ✅ **Incremental Updates**: Rescan only changed files

## 🏗️ Architecture Overview

### Three Main Components:

#### 1. Scanner Engine
**Purpose**: Extract all metadata from files
**Technologies**: Python, Pillow, PyPDF2, mutagen, exifread, pefile
**Output**: Normalized metadata → SQLite database

#### 2. Database Layer
**Purpose**: Store and query metadata efficiently
**Technologies**: SQLite with FTS5 (full-text search)
**Schema**: Flexible JSON columns + indexed common fields

#### 3. Filter UI
**Purpose**: Beautiful, responsive filtering interface
**Technologies**: CustomTkinter (native feel, fast)
**Features**: Real-time filtering, saved queries, export results

### Data Flow:
```
Files → Scanner → Extractors → Normalizer → Database
                                               ↓
                                          Query Engine
                                               ↓
                                           Filter UI
```

## 📊 Metadata Categories

### File Types & Metadata:

#### 1. Images (JPEG, PNG, RAW, etc.)
**Metadata Fields (~45)**:
- Camera: Make, model, serial number
- Settings: ISO, aperture, shutter speed, focal length
- GPS: Latitude, longitude, altitude, location name
- Dates: Taken, modified, digitized
- Dimensions: Width, height, resolution, orientation
- Colors: Dominant colors, color space, bit depth

**Filter Examples**:
- "Photos from Canon 5D Mark IV"
- "Images taken in 2024 in Paris"
- "Landscape orientation photos"
- "High ISO shots (>3200)"

#### 2. Documents (PDF, Word, Excel, PowerPoint)
**Metadata Fields (~30)**:
- Author: Name, company, manager
- Content: Page count, word count, character count
- Dates: Created, modified, printed
- Properties: Title, subject, keywords, category
- Technical: Software used, template, revision number

**Filter Examples**:
- "PDFs by John Smith over 50 pages"
- "Word docs from ProjectX folder"
- "Excel files with >10 sheets"
- "Presentations modified this week"

#### 3. Audio (MP3, FLAC, WAV, etc.)
**Metadata Fields (~35)**:
- Music: Artist, album, title, genre, year
- Technical: Duration, bitrate, sample rate, codec
- Advanced: BPM, key, mood, lyrics
- Organization: Track number, disc number, composer

**Filter Examples**:
- "Rock songs from 2020-2024"
- "High quality audio (>320kbps)"
- "Songs 140-160 BPM for running"
- "Tracks longer than 5 minutes"

#### 4. Video (MP4, MKV, AVI, etc.)
**Metadata Fields (~30)**:
- Video: Codec, resolution, FPS, bitrate, duration
- Audio: Codec, channels, language tracks
- Content: Title, description, genre, year
- Technical: Container format, aspect ratio

**Filter Examples**:
- "4K videos"
- "Movies longer than 90 minutes"
- "Videos with 5.1 surround sound"
- "H.265 encoded files"

#### 5. Executables (.exe, .dll)
**Metadata Fields (~25)**:
- Version: File version, product version
- Company: Name, product name, description
- Security: Digital signature, signer, certificate
- Technical: Architecture (x86/x64), subsystem

**Filter Examples**:
- "Microsoft signed executables"
- "64-bit applications"
- "Programs from 2024"
- "Tools by Adobe"

#### 6. Archives (ZIP, RAR, 7Z)
**Metadata Fields (~15)**:
- Compression: Method, ratio, original size
- Contents: File count, folder count
- Security: Encrypted, password protected
- Technical: Format version, creator software

**Filter Examples**:
- "Encrypted archives"
- "Large archives (>100 files)"
- "High compression ratio (>50%)"
- "RAR files created this month"

#### 7. Source Code (Python, JavaScript, Java, etc.)
**Metadata Fields (~20)**:
- Language: Detected language, version hints
- Metrics: Lines of code, comments, complexity
- Content: Function count, class count, imports
- Quality: TODO count, documentation present

**Filter Examples**:
- "Python files with >500 lines"
- "JavaScript with >30% comments"
- "Files with TODO markers"
- "Source files from last week"

#### 8. CAD Files (DWG, DXF, SKP)
**Metadata Fields (~15)**:
- Properties: Title, author, project name
- Technical: Software, version, units
- Content: Layer count, entity count
- Dates: Created, modified

**Filter Examples**:
- "AutoCAD 2024 drawings"
- "DWG files for Building-A project"
- "Drawings in metric units"
- "Files by architect@company.com"

## 🎨 UI Design Concept

### Main Window Layout:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📁 MetaFinder                          [Scan] [⚙️] ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                      ┃
┃  🔍 Quick Search: [________________] 🎯 Advanced    ┃
┃                                                      ┃
┃  📊 Active Filters (4):                             ┃
┃    [Extension: .jpg ✕] [Camera: Canon ✕]           ┃
┃    [Year: 2024 ✕] [GPS: Paris ✕]                   ┃
┃    [Clear All]                                       ┃
┃                                                      ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ FILTERS                │  RESULTS (1,234 files)     ┃
┃━━━━━━━━━━━━━━━━━━━━━━│━━━━━━━━━━━━━━━━━━━━━━━━━━━┃
┃                        │                             ┃
┃ 📁 File Type           │ 📄 vacation.jpg            ┃
┃   □ Images (5,234)     │    Canon EOS 5D Mark IV    ┃
┃   ☑ Documents (2,145)  │    Paris, France           ┃
┃   □ Audio (1,892)      │    2024-06-15 14:32        ┃
┃   □ Video (234)        │    3.2 MB, 4000x3000       ┃
┃   □ Archives (178)     │    [Open] [Show in Folder] ┃
┃                        │                             ┃
┃ 📅 Date Range          │ 📄 meeting-notes.pdf       ┃
┃   ○ Any time           │    Adobe Acrobat           ┃
┃   ● Custom range:      │    John Smith              ┃
┃   From: [2024-01-01]   │    2024-09-10 09:15        ┃
┃   To:   [2024-12-31]   │    24 pages, 1.8 MB        ┃
┃                        │    [Open] [Show in Folder] ┃
┃ 📏 Size                │                             ┃
┃   [===========|====]   │ 📄 song.mp3                ┃
┃   10 KB - 100 MB       │    Artist: The Beatles     ┃
┃                        │    Album: Abbey Road        ┃
┃ 📸 Camera              │    Duration: 3:45           ┃
┃   [Canon_______|v]     │    320 kbps MP3            ┃
┃                        │    [Open] [Show in Folder] ┃
┃ 👤 Author              │                             ┃
┃   [John Smith__|v]     │ ... (scroll for more)      ┃
┃                        │                             ┃
┃ 🌍 GPS Location        │ [Prev] [1-50 of 1234] [Next]┃
┃   [Paris_______|v]     │                             ┃
┃                        │                             ┃
┃ [+ Add Custom Filter]  │ [Export Results]            ┃
┗━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Filter Panel Features:
1. **Collapsible Categories**: Expand/collapse filter groups
2. **Multi-Select**: Check multiple values (OR logic)
3. **Range Sliders**: For size, date, numeric fields
4. **Auto-Complete**: For text fields (author, camera, etc.)
5. **Filter Count**: Show how many files match each filter
6. **Real-Time**: Results update as you filter
7. **Saved Queries**: Save frequently used filter combinations

### Results Panel Features:
1. **Card View**: Rich preview with metadata
2. **List View**: Compact table view
3. **Thumbnail View**: Grid of thumbnails (images/videos)
4. **Sort Options**: By name, date, size, relevance
5. **Quick Actions**: Open, show in folder, copy path
6. **Batch Operations**: Select multiple files
7. **Export**: Save results to CSV/JSON

## 🔧 Technical Implementation

### Phase 1: Scanner Engine (Week 1)
**Goal**: Extract all metadata from common file types

#### Extractors to Build:
1. **ImageExtractor** (Pillow, exifread)
   - EXIF data from JPEG/PNG
   - GPS coordinates with geocoding
   - Color analysis
   - Thumbnail generation

2. **DocumentExtractor** (PyPDF2, python-docx, openpyxl)
   - PDF metadata and text
   - Word/Excel/PowerPoint properties
   - Page/word counts

3. **AudioExtractor** (mutagen)
   - ID3 tags from MP3/FLAC/M4A
   - Technical properties
   - BPM detection (optional)

4. **VideoExtractor** (ffmpeg-python)
   - Container and codec info
   - Resolution, FPS, duration
   - Audio tracks

5. **ExecutableExtractor** (pefile)
   - Version information
   - Digital signatures
   - Architecture

6. **ArchiveExtractor** (zipfile, rarfile, py7zr)
   - Contents list
   - Compression stats
   - Encryption status

7. **CodeExtractor** (pygments)
   - Language detection
   - Line/function counts
   - Complexity metrics

#### Database Schema:
```sql
CREATE TABLE files (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    extension TEXT,
    size INTEGER,
    created REAL,
    modified REAL,
    accessed REAL,

    -- Common indexed fields
    file_type TEXT, -- 'image', 'document', 'audio', etc.
    author TEXT,
    title TEXT,
    date_taken REAL,

    -- Full metadata as JSON
    metadata TEXT, -- Complete metadata as JSON

    -- Full-text search
    searchable_text TEXT, -- All text combined for FTS

    -- Indexing
    scan_date REAL,
    hash TEXT
);

CREATE VIRTUAL TABLE files_fts USING fts5(
    name, author, title, keywords, content
);

CREATE INDEX idx_file_type ON files(file_type);
CREATE INDEX idx_extension ON files(extension);
CREATE INDEX idx_size ON files(size);
CREATE INDEX idx_date ON files(modified);
CREATE INDEX idx_author ON files(author);
```

#### Metadata JSON Structure:
```json
{
  "basic": {
    "path": "/path/to/file.jpg",
    "size": 3145728,
    "modified": 1705939200.0
  },
  "image": {
    "camera": {
      "make": "Canon",
      "model": "EOS 5D Mark IV",
      "serial": "123456"
    },
    "settings": {
      "iso": 400,
      "aperture": 2.8,
      "shutter": "1/250",
      "focal_length": 50
    },
    "gps": {
      "latitude": 48.8566,
      "longitude": 2.3522,
      "location": "Paris, France"
    },
    "dimensions": {
      "width": 4000,
      "height": 3000,
      "orientation": "landscape"
    }
  }
}
```

### Phase 2: Database Layer (Week 1)
**Goal**: Fast, flexible querying

#### Query Builder:
```python
class QueryBuilder:
    def filter_by_type(self, file_type: str)
    def filter_by_extension(self, extensions: List[str])
    def filter_by_size(self, min_size: int, max_size: int)
    def filter_by_date(self, start: datetime, end: datetime)
    def filter_by_author(self, authors: List[str])
    def filter_by_metadata(self, json_path: str, value: Any)
    def full_text_search(self, query: str)
    def combine_filters(self, mode: 'AND' | 'OR')
    def execute(self) -> List[FileResult]
```

#### Performance Targets:
- Initial scan: 60,000 files in 5-10 minutes
- Query response: <100ms for any filter combination
- Database size: ~5 KB per file (300 MB for 60k files)
- Incremental rescan: <1 minute for changed files

### Phase 3: Filter UI (Week 2)
**Goal**: Beautiful, responsive filtering

#### Features:
1. **Dynamic Filters**: Filters appear based on available metadata
2. **Filter Counts**: Show result count for each filter option
3. **Real-Time Updates**: Results refresh as you type/select
4. **Saved Queries**: Name and save filter combinations
5. **Export Options**: CSV, JSON, file list
6. **Batch Actions**: Open multiple, copy paths, delete

#### UI Components:
- **FilterPanel**: Left sidebar with all filter options
- **ResultsPanel**: Main area showing matching files
- **PreviewPanel**: Right sidebar with file details
- **QuickSearch**: Top bar for keyword search
- **StatusBar**: Show filter count, results count, selection

## 🎯 Feature Roadmap

### v1.0 - Core Features (3 weeks)
- ✅ Scan folder and extract basic metadata
- ✅ SQLite database with FTS5
- ✅ Basic filter UI (type, extension, size, date)
- ✅ Results list with open/show actions
- ✅ Image EXIF extraction
- ✅ Document metadata extraction
- ✅ Audio ID3 tags

### v1.1 - Enhanced Filtering (2 weeks)
- ✅ Advanced filters (camera, author, GPS)
- ✅ Saved queries
- ✅ Export results
- ✅ Video metadata
- ✅ Executable version info
- ✅ Archive contents

### v1.2 - Polish & Performance (1 week)
- ✅ Incremental rescan (only changed files)
- ✅ Background indexing
- ✅ Thumbnail cache
- ✅ Better error handling
- ✅ Progress indicators

### v2.0 - Advanced Features (Future)
- ⏳ Multiple folder catalogs
- ⏳ Cloud storage scanning (Google Drive, Dropbox)
- ⏳ Network share support
- ⏳ Duplicate detection
- ⏳ Tag management (user-defined tags)
- ⏳ Smart collections
- ⏳ Statistics dashboard

### v3.0 - Power User Features (Future)
- ⏳ SQL query editor for advanced users
- ⏳ API for external tools
- ⏳ Plugins system
- ⏳ Batch metadata editing
- ⏳ Relationship graphs
- ⏳ Watch folders (auto-rescan on changes)

## 🎨 UI/UX Priorities

### Must Have:
1. **Fast**: Filters respond instantly (<100ms)
2. **Clear**: Obvious what each filter does
3. **Forgiving**: Easy to undo filters
4. **Discoverable**: Users find features naturally
5. **Informative**: Show counts, previews, details

### Nice to Have:
1. **Keyboard Shortcuts**: Power user navigation
2. **Dark/Light Theme**: User preference
3. **Column Customization**: Choose what to display
4. **Sort & Group**: Flexible result organization
5. **Preview Pane**: Quick look without opening

## 💾 Data & Storage

### Database Files:
```
catalog.db        -- SQLite database (300 MB for 60k files)
thumbnails/       -- Cached thumbnails (optional, ~2 GB)
queries/          -- Saved queries (JSON files)
config.json       -- App settings
```

### Performance Considerations:
- Use PRAGMA for SQLite optimization
- Index frequently filtered fields
- Lazy-load thumbnails
- Paginate results (50-100 per page)
- Cache common queries

## 🚀 Success Metrics

### User Goals:
1. **Find any file in <10 seconds** using filters
2. **Scan 60,000 files in <10 minutes**
3. **Filter results appear in <100ms**
4. **Learn the interface in <5 minutes**

### Technical Goals:
1. **Extract 90+ metadata fields** per file type
2. **Support 20+ file formats**
3. **Handle 100,000+ files** without slowdown
4. **Use <500 MB RAM** during normal operation

## 🎬 Launch Strategy

### Target Users:
1. **Photographers**: Find photos by camera, GPS, settings
2. **Content Creators**: Organize media by metadata
3. **Developers**: Search code by language, metrics
4. **Document Workers**: Find docs by author, page count
5. **Data Hoarders**: Organize massive file collections

### Key Selling Points:
- ✅ No AI needed (fast, reliable, offline)
- ✅ Instant results (database queries)
- ✅ Rich metadata (90+ fields per file)
- ✅ Beautiful UI (modern, intuitive)
- ✅ Non-destructive (never touch original files)
- ✅ One-time scan (never wait again)

## 🔮 Future Vision

### Long-Term Goals:
1. **Universal File Finder**: The go-to tool for finding any file
2. **Platform Expansion**: Windows → Mac → Linux
3. **Cloud Integration**: Google Drive, Dropbox, OneDrive
4. **Mobile Apps**: Browse your catalog on phone/tablet
5. **Enterprise Version**: Network shares, collaboration
6. **Plugin Ecosystem**: Community-created extractors

## 📝 Technical Challenges & Solutions

### Challenge 1: Large Folders (1M+ files)
**Solution**:
- Stream processing (don't load all into memory)
- Parallel extraction (multi-threading)
- Progress checkpoints (resume on crash)

### Challenge 2: Slow Metadata Extraction
**Solution**:
- Prioritize common fields
- Skip expensive operations (ML, OCR) by default
- Background processing (scan while user works)

### Challenge 3: Database Size
**Solution**:
- Compress JSON metadata
- Configurable extraction depth
- Purge old scan data

### Challenge 4: UI Responsiveness
**Solution**:
- Async queries (never block UI)
- Result pagination
- Virtual scrolling
- Lazy thumbnail loading

## 🎯 Core Differentiators

### vs. Windows Search:
- ✅ **100x more metadata** (Windows only indexes basic fields)
- ✅ **Advanced filtering** (Windows has limited filters)
- ✅ **Beautiful UI** (Windows search is basic)
- ✅ **Reliable** (Windows search index breaks often)

### vs. Everything (voidtools):
- ✅ **Rich metadata** (Everything only indexes names/paths)
- ✅ **Smart filtering** (Everything is text search only)
- ✅ **File-type specific** (Everything treats all files the same)

### vs. File Organizer Pro:
- ✅ **Search-focused** (File Organizer is organization-focused)
- ✅ **Filter-based** (File Organizer creates views)
- ✅ **Instant results** (File Organizer processes on demand)

## 📋 Next Steps

### Immediate (This Session):
1. ✅ Create brainstorm document
2. ⏳ Create GitHub repository
3. ⏳ Design database schema
4. ⏳ Prototype Scanner Engine
5. ⏳ Create basic UI wireframe

### Week 1:
1. Implement core extractors (Image, Document, Audio)
2. Build database layer
3. Create basic filter UI
4. Test with sample files

### Week 2:
1. Add more extractors (Video, Executable, Archive)
2. Implement saved queries
3. Polish UI/UX
4. Add export functionality

### Week 3:
1. Performance optimization
2. Error handling
3. Documentation
4. First release

---

## 🎉 Project Name: MetaFinder

**Tagline**: "Find Any File, Filter by Everything"

**Mission**: Make every file's metadata accessible and searchable, so you never have to manually organize files again.

**Vision**: The universal file finder that knows everything about your files and helps you find exactly what you need in seconds.

---

**Ready to Build! 🚀**
