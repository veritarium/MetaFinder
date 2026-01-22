# MetaFinder Testing Guide

Guide for testing MetaFinder with real files on your local machine.

## 🎯 Testing Goals

1. **Verify metadata extraction works** across different file types
2. **Test GUI functionality** (scan, filter, search, display)
3. **Validate performance** with real-world file counts
4. **Identify bugs** and edge cases
5. **Gather user feedback** on UX

## 📋 Prerequisites

### 1. Install ExifTool

**macOS:**
```bash
brew install exiftool
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install libimage-exiftool-perl
```

**Windows:**
1. Download from https://exiftool.org/
2. Extract `exiftool.exe` to a folder
3. Add folder to PATH environment variable

### 2. Verify Installation

```bash
exiftool -ver
```

Should show version 12.15 or higher.

### 3. Install Python Dependencies

```bash
cd MetaFinder
pip3 install -r requirements.txt
```

## 🧪 Test Scenarios

### Test 1: Basic Functionality Check

**Goal**: Verify all components work

**Steps**:
1. Run test suite:
   ```bash
   python3 test_prototype.py
   ```

2. Expected: All tests pass (4/4)

3. If any fail, note the error and environment details

### Test 2: CLI Scan Test

**Goal**: Test command-line scanning

**Steps**:
1. Create a test folder with sample files:
   ```bash
   mkdir ~/metafinder-test
   # Add some photos, PDFs, music files
   ```

2. Scan the folder:
   ```bash
   python3 metafinder_cli.py scan ~/metafinder-test
   ```

3. Check statistics:
   ```bash
   python3 metafinder_cli.py stats
   ```

4. Search for files:
   ```bash
   python3 metafinder_cli.py search --type image
   ```

**Expected Results**:
- Scan completes without errors
- Statistics show correct file counts
- Search returns matching files

**Record**:
- Number of files scanned
- Scan duration
- Any errors encountered

### Test 3: GUI Basic Test

**Goal**: Verify GUI launches and works

**Steps**:
1. Launch GUI:
   ```bash
   python3 metafinder_gui.py
   ```

2. Verify:
   - Window opens without errors
   - Interface is responsive
   - All buttons are clickable
   - Filter dropdowns work

**Expected**:
- GUI opens in dark mode
- Welcome message displayed
- Status bar shows "Ready"

**Record**:
- Launch time
- Any visual glitches
- Performance issues

### Test 4: Small Folder Scan (GUI)

**Goal**: Test scanning with GUI

**Test Folder**: 10-50 files (photos, documents, music)

**Steps**:
1. Launch GUI
2. Click "Scan Folder"
3. Select test folder
4. Confirm scan
5. Wait for completion

**Monitor**:
- Progress updates appear
- Percentage advances correctly
- UI remains responsive
- No freezing

**After Scan**:
- Check statistics (click Statistics button)
- Verify file count matches
- Try applying filters
- Click on result cards
- Try "Open" button

**Record**:
- Scan duration
- Files processed
- Any errors
- UI responsiveness (smooth/laggy)

### Test 5: Medium Folder Scan

**Goal**: Test with realistic file count

**Test Folder**: 500-1000 files mixed types

**Steps**:
1. Scan folder with GUI
2. Test filtering by:
   - File type (image, document, audio)
   - Extension (.jpg, .pdf, .mp3)
   - Author (if available in files)
   - Camera (for photos)

**Record**:
- Scan duration
- Query response time
- Filter accuracy
- Memory usage (Task Manager/Activity Monitor)

### Test 6: Large Folder Scan (Optional)

**Goal**: Stress test with many files

**Test Folder**: 5,000+ files (like Pictures folder)

**Steps**:
1. Scan with GUI
2. Monitor progress carefully
3. Test search performance

**Watch For**:
- Memory usage
- Scan completion
- Database size (in data/ folder)
- Search speed still fast

**Record**:
- Total files scanned
- Total duration
- Database file size
- Any performance degradation

### Test 7: Filter Accuracy Test

**Goal**: Verify metadata extraction and filtering

**Prepare Test Files**:
- 5-10 JPEG photos (with EXIF data)
- 5-10 PDF documents (with author metadata)
- 5-10 MP3 files (with ID3 tags)

**Steps**:
1. Scan folder
2. Filter by Type = "image"
   - Should show only JPEGs
3. Filter by Camera (if available)
   - Should show only matching camera
4. Clear filters
5. Filter by Type = "document"
   - Should show only PDFs
6. Enter author name
   - Should filter to matching documents

**Record**:
- Filter accuracy (correct results?)
- False positives/negatives
- Missing metadata

### Test 8: Metadata Completeness

**Goal**: Verify metadata extraction quality

**Steps**:
1. Use CLI to get detailed file info:
   ```bash
   python3 metafinder_cli.py info /path/to/photo.jpg --verbose
   ```

2. Compare with ExifTool directly:
   ```bash
   exiftool /path/to/photo.jpg
   ```

**Check**:
- Camera make/model extracted?
- Date taken correct?
- GPS coordinates (if present)?
- Author/artist info?
- File size accurate?

**Record**:
- Fields extracted correctly
- Fields missing
- Fields with wrong values

### Test 9: Edge Cases

**Goal**: Find bugs with unusual files

**Test With**:
- Very large files (>1GB video)
- Files with no metadata
- Corrupted files
- Files with special characters in names
- Very long filenames
- Nested folders (10+ levels deep)

**Steps**:
1. Scan folder with edge case files
2. Note any errors or crashes
3. Verify files appear in results
4. Check error handling

**Record**:
- Crashes encountered
- Error messages
- Files that failed to scan

### Test 10: User Workflow Test

**Goal**: Realistic usage scenario

**Scenario**: "Find all photos taken with my camera last month"

**Steps**:
1. Launch GUI
2. Scan your actual Photos folder
3. Filter:
   - Type = image
   - Camera = (your camera)
   - (Ideally date range, not implemented yet)
4. Browse results
5. Open a few files

**Evaluate**:
- Was it easy to do?
- Were results accurate?
- Any confusion about UI?
- Missing features noticed?

## 📊 Test Report Template

After testing, fill out this report:

```markdown
# MetaFinder Test Report

**Date**: YYYY-MM-DD
**Tester**: Your Name
**System**: OS, Python version, ExifTool version

## Summary
- [ ] CLI works
- [ ] GUI launches
- [ ] Scanning works
- [ ] Filtering works
- [ ] No crashes

## Test Results

### Test 1: Basic Functionality
- Status: PASS/FAIL
- Notes: ...

### Test 2: CLI Scan
- Files scanned: X
- Duration: Y seconds
- Status: PASS/FAIL
- Errors: ...

### Test 3: GUI Launch
- Status: PASS/FAIL
- Issues: ...

### Test 4: Small Scan (GUI)
- Files: X
- Duration: Y
- Status: PASS/FAIL
- Notes: ...

### Test 5-10: ...

## Bugs Found

1. Bug description
   - How to reproduce
   - Expected vs actual behavior
   - Severity: Low/Medium/High

2. ...

## Performance Observations

- Scan speed: X files/second
- Query response: <100ms / >100ms
- Memory usage: X MB during scan
- UI responsiveness: Smooth / Laggy

## User Experience Feedback

### What Works Well:
- ...

### What Needs Improvement:
- ...

### Missing Features Noticed:
- ...

### Suggestions:
- ...

## Overall Assessment

- [ ] Ready for use
- [ ] Needs minor fixes
- [ ] Needs major fixes
- [ ] Not ready

**Recommendation**: ...
```

## 🐛 Known Limitations (v0.1 Prototype)

Things we know don't work yet:
1. No date range picker (filter by date range)
2. No thumbnail preview
3. No saved queries
4. No export to CSV/JSON
5. No incremental scan (rescan all files)
6. Results limited to 100
7. No duplicate detection
8. No batch file operations
9. No GPS location filtering (data extracted but not filterable yet)

## 📝 Reporting Issues

If you find bugs, please report with:
1. **Description**: What happened?
2. **Expected**: What should happen?
3. **Steps to reproduce**: How to trigger the bug?
4. **System info**: OS, Python version, ExifTool version
5. **Files involved**: What types of files?
6. **Error messages**: Any error text or screenshots

Create issues at: (GitHub Issues link)

## 🎯 Success Criteria

The prototype is successful if:
- ✅ Can scan 1000+ files without crashing
- ✅ Metadata extracted correctly for common file types
- ✅ Filters work and return accurate results
- ✅ GUI is usable and responsive
- ✅ Search results appear in <1 second
- ✅ No data loss or corruption

## 🚀 Next Steps After Testing

Based on test results, we'll prioritize:
1. Bug fixes (highest priority)
2. Performance improvements
3. Missing metadata fields
4. UI/UX improvements
5. Feature additions

## 💡 Tips for Effective Testing

1. **Start small**: Test with 10-50 files first
2. **Use real files**: Your actual photos/documents
3. **Take notes**: Document everything
4. **Test edge cases**: Unusual files, long names, etc.
5. **Check metadata**: Compare with ExifTool directly
6. **Monitor resources**: Watch CPU/RAM usage
7. **Try workflows**: Realistic user scenarios
8. **Be thorough**: Click everything!

## 📞 Need Help?

If you encounter issues during testing:
1. Check PROTOTYPE_README.md for setup instructions
2. Verify ExifTool is installed correctly
3. Check Python dependencies are installed
4. Look for error messages in terminal
5. Report issues with details

---

**Happy Testing! 🧪**

Your feedback is invaluable for improving MetaFinder.
