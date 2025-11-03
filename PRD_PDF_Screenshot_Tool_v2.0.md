# PRD: PDF Screenshot Tool - Enhanced Version 2.0

## 📋 Product Overview

**Product Name:** PDF Screenshot Tool v2.0  
**Platform:** macOS only  
**Interface:** Graphical User Interface (GUI) using tkinter  
**Current Version:** v1.0 (CLI-based)  
**Target Version:** v2.0 (GUI-based with flexible screenshot regions)

---

## 🎯 Goals & Objectives

### Primary Goals
1. **Flexible Screenshot Region** - Allow users to define custom screenshot coordinates for different PDF formats
2. **User-Friendly GUI** - Transform command-line tool into a native macOS application
3. **Maintain Core Functionality** - Keep all existing features (screenshots, PNG→PDF conversion, combined workflow)

### Success Metrics
- ✅ Users can set custom screenshot regions without editing code
- ✅ Application launches with double-click (.app bundle)
- ✅ No terminal/command-line knowledge required
- ✅ Same reliability as v1.0

---

## 👥 Target Users

**Primary User:** You (adamartinik)
- macOS user
- Works with various PDF formats requiring different crop regions
- Needs quick, repeatable PDF processing workflow
- Tech-savvy but prefers GUI over CLI for this task

**Secondary Users:** 
- Anyone you share the tool with (no Python knowledge required)
- Users who need to extract specific regions from multi-page PDFs

---

## ✨ Features & Requirements

### 🆕 New Features (v2.0)

#### 1. Custom Screenshot Region Input
**Priority:** HIGH (MVP)

**User Story:** As a user, I want to define the screenshot area for each PDF document, so I can handle different PDF formats and layouts.

**Acceptance Criteria:**
- [ ] User can input coordinates via GUI
- [ ] Two input methods:
  - **Method A:** Enter 4 values: X1, Y1 (top-left) and X2, Y2 (bottom-right)
  - **Method B:** Visual selection tool (click and drag on screen)
- [ ] Input validation (coordinates must be positive integers, X2>X1, Y2>Y1)
- [ ] Live preview of selected region dimensions (width × height in pixels)
- [ ] Default values suggested (current: 880, 180, 840, 1150)
- [ ] Option to test screenshot region before batch processing

**Technical Notes:**
- Convert (X1, Y1, X2, Y2) to pyautogui format (x, y, width, height)
- Width = X2 - X1
- Height = Y2 - Y1

---

#### 2. Graphical User Interface (GUI)
**Priority:** HIGH (MVP)

**User Story:** As a user, I want a visual interface with buttons and forms, so I don't need to use the terminal.

**Acceptance Criteria:**
- [ ] Main window with clear sections for each operation
- [ ] Three main tabs/sections:
  - 📸 "Screenshot PDF"
  - 📄 "PNG to PDF"
  - 🚀 "Complete Process"
- [ ] Input fields for:
  - Number of pages
  - Output folder name
  - Screenshot coordinates (X1, Y1, X2, Y2)
- [ ] Progress bar during processing
- [ ] Status messages (success/error notifications)
- [ ] "Start" button with countdown preview
- [ ] "Cancel" button to stop processing

**UI Mockup (Text-based):**
```
┌─────────────────────────────────────────────────┐
│  PDF Screenshot Tool v2.0                    [X]│
├─────────────────────────────────────────────────┤
│  [📸 Screenshots] [📄 PNG→PDF] [🚀 Complete]   │
├─────────────────────────────────────────────────┤
│                                                  │
│  Screenshot Region Settings                      │
│  ┌──────────────────────────────────────────┐  │
│  │ Top-Left Corner:                          │  │
│  │   X1: [880    ]  Y1: [180    ]           │  │
│  │                                           │  │
│  │ Bottom-Right Corner:                      │  │
│  │   X2: [1720   ]  Y2: [1330   ]           │  │
│  │                                           │  │
│  │ → Region: 840×1150 pixels                │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  [Test Region] [Visual Selector]                │
│                                                  │
│  PDF Processing                                  │
│  Number of pages: [____]                        │
│  Output folder: [________________]              │
│                                                  │
│  [Start Processing]  [Cancel]                   │
│                                                  │
│  Status: Ready                                   │
│  ▓▓▓▓▓▓▓▓░░░░░░░░░░ 45%                        │
└─────────────────────────────────────────────────┘
```

---

#### 3. Standalone macOS Application
**Priority:** HIGH (MVP)

**User Story:** As a user, I want to launch the app with a double-click, so I don't need Python or terminal access.

**Acceptance Criteria:**
- [ ] Build `.app` bundle using PyInstaller or py2app
- [ ] Application icon (custom .icns file)
- [ ] All dependencies bundled (pyautogui, Pillow, tkinter)
- [ ] No Python installation required to run
- [ ] Launches from Finder with double-click
- [ ] Works on macOS 11+ (Big Sur and newer)

**Build Process:**
```bash
# Using PyInstaller
pyinstaller --onefile --windowed --name="PDF Screenshot Tool" \
  --icon=icon.icns supertool_v2.py

# Or using py2app
python setup.py py2app
```

---

### 🔄 Existing Features (Keep from v1.0)

#### 4. Automated PDF Screenshots
**Priority:** HIGH (MVP)

- [x] Take screenshots of open PDF document
- [x] Navigate through pages automatically (arrow key simulation)
- [x] Save as numbered PNG files (strana_01.png, strana_02.png, etc.)
- [x] Create organized folder on Desktop
- [x] Countdown before starting (5 seconds)

**Changes from v1.0:**
- ✅ Keep: Core functionality
- ⚠️ Update: Screenshot region now user-defined (not hardcoded)
- ⚠️ Update: GUI replaces CLI menu

---

#### 5. PNG to PDF Conversion
**Priority:** HIGH (MVP)

- [x] Convert series of PNG images to single PDF
- [x] Browse and select folder with PNG files
- [x] Maintain image order (alphabetical/numerical)
- [x] RGB conversion for PDF compatibility
- [x] Display file size and page count

**Changes from v1.0:**
- ✅ Keep: Core functionality unchanged
- ⚠️ Update: Folder selection via GUI file browser

---

#### 6. Combined Workflow
**Priority:** MEDIUM

- [x] Screenshots → PNG → PDF in one process
- [x] Option to delete PNG files after PDF creation
- [x] Option to open final PDF

**Changes from v1.0:**
- ✅ Keep: Workflow logic
- ⚠️ Update: GUI buttons instead of Y/N prompts

---

### 💡 Nice-to-Have Features (Future v2.1+)

**Not in v2.0 scope, but document for later:**

1. **Visual Region Selector** (drag & drop on screen)
   - Click and drag to select screenshot area
   - Live overlay showing selected region
   - Automatic coordinate capture

2. **Preset Management**
   - Save named presets (e.g., "A4 Portrait", "Letter Landscape")
   - Quick load from dropdown
   - Export/import preset file

3. **Batch Multiple PDFs**
   - Process multiple PDF files in sequence
   - Queue management

4. **Auto-detection of PDF boundaries**
   - Smart crop detection
   - Remove white margins automatically

5. **Preview Window**
   - Show first page with overlay of screenshot region
   - Visual confirmation before processing

---

## 🛠️ Technical Requirements

### Technology Stack
- **Language:** Python 3.9+
- **GUI Framework:** tkinter (built into Python)
- **Dependencies:**
  - `pyautogui` - screenshot automation
  - `Pillow (PIL)` - image processing
  - `pathlib` - file system operations
- **Build Tool:** PyInstaller or py2app
- **Platform:** macOS 11+ (Big Sur and newer)

### Architecture Changes

**v1.0 Structure:**
```
CLI Menu → Function Selection → Processing → Terminal Output
```

**v2.0 Structure:**
```
GUI Window → Tabs/Sections → Input Forms → Processing → GUI Updates
```

### File Structure
```
pdf-screenshot-tool/
├── supertool_v2.py          # Main application with GUI
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── .gitignore               # Git ignore rules
├── build/                   # Build artifacts (gitignored)
├── dist/                    # Distribution files (gitignored)
│   └── PDF Screenshot Tool.app  # macOS application
├── assets/                  # Application assets
│   └── icon.icns           # App icon
└── setup.py                 # Build configuration
```

---

## 🎨 User Experience Flow

### Main Flow: Screenshot with Custom Region

1. **Launch App** (double-click `PDF Screenshot Tool.app`)
2. **See Main Window** with three tabs
3. **Navigate to "Screenshots" tab**
4. **Set Screenshot Region:**
   - See default values (880, 180, 1720, 1330)
   - Option A: Modify coordinates manually
   - Option B: Click "Visual Selector" (future feature)
   - See calculated dimensions (840×1150 px)
5. **Test Region** (optional):
   - Click "Test Region" button
   - Takes one test screenshot
   - Shows preview
6. **Configure Processing:**
   - Enter number of pages
   - Enter output folder name
7. **Start Processing:**
   - Click "Start Processing"
   - See 5-second countdown
   - Watch progress bar
   - See status updates
8. **Complete:**
   - See success message
   - Option to open folder
   - Option to continue with PNG→PDF conversion

### Alternative Flow: Direct PNG→PDF

1. Launch app
2. Navigate to "PNG→PDF" tab
3. Click "Browse Folder"
4. Select folder with PNG files
5. See file preview (first 5 files)
6. Enter PDF output name
7. Click "Create PDF"
8. See progress bar
9. Success notification with file location

---

## 🚫 Non-Goals (Out of Scope for v2.0)

- ❌ Windows/Linux support
- ❌ Cloud storage integration
- ❌ OCR or text extraction
- ❌ PDF editing features
- ❌ Preset saving/loading
- ❌ Advanced visual region selector (drag & drop)
- ❌ Batch processing multiple PDFs
- ❌ Auto-update functionality
- ❌ Multi-language support
- ❌ Online documentation/help system

---

## ✅ Acceptance Criteria (Definition of Done)

**v2.0 is complete when:**

1. ✅ GUI launches successfully on macOS
2. ✅ User can input custom screenshot coordinates (X1, Y1, X2, Y2)
3. ✅ Coordinate validation works correctly
4. ✅ Dimension preview calculates accurately
5. ✅ Screenshot automation works with custom regions
6. ✅ Progress bar updates during processing
7. ✅ PNG→PDF conversion works through GUI
8. ✅ Application builds as standalone `.app` bundle
9. ✅ .app launches without Python installation
10. ✅ All v1.0 features still functional
11. ✅ No crashes or errors during normal usage
12. ✅ README updated with v2.0 instructions

---

## 📅 Development Phases

### Phase 1: Core GUI Implementation
**Deliverable:** Working GUI with all input fields

- Create main window with tkinter
- Add tabs for different operations
- Implement coordinate input fields
- Add validation logic
- Create progress indicators

### Phase 2: Feature Integration
**Deliverable:** GUI connected to existing functions

- Connect GUI to screenshot_pdf()
- Connect GUI to png_to_pdf()
- Connect GUI to combined workflow
- Update functions to accept GUI parameters
- Replace print() with GUI status updates

### Phase 3: Testing & Refinement
**Deliverable:** Polished, tested application

- Test all workflows
- Fix bugs
- Improve error handling
- Add helpful error messages
- Test coordinate edge cases

### Phase 4: Standalone Build
**Deliverable:** Distributable `.app` file

- Create app icon
- Configure PyInstaller/py2app
- Build .app bundle
- Test on clean macOS system
- Create installation instructions

---

## 🐛 Known Limitations

1. **macOS Only** - Will not run on Windows/Linux
2. **Active PDF Window Required** - PDF must be visible and active for screenshots
3. **Fixed Navigation** - Uses arrow key (down) - assumes standard PDF viewer behavior
4. **No Preset Saving** - Coordinates must be entered each time
5. **Manual Region Definition** - No automatic boundary detection

---

## 📦 Deliverables

1. **supertool_v2.py** - Main application file with GUI
2. **PDF Screenshot Tool.app** - Standalone macOS application
3. **README.md** - Updated documentation including:
   - v2.0 feature list
   - Installation instructions
   - Usage guide with screenshots
   - How to set custom regions
   - Troubleshooting
4. **requirements.txt** - Python dependencies
5. **Build instructions** - How to create .app bundle

---

## 🚀 Success Criteria

**v2.0 is successful if:**

1. You can process PDFs with different formats without editing code
2. Application launches reliably with double-click
3. GUI is intuitive and requires no documentation for basic use
4. All v1.0 functionality preserved
5. Processing time similar to v1.0 (no performance degradation)
6. Works on your macOS system without issues

---

## 📝 Notes & Considerations

### GUI Framework Choice: tkinter
**Why tkinter?**
- ✅ Built into Python (no extra dependencies)
- ✅ Works well on macOS
- ✅ Simple for our use case
- ✅ Easy to bundle in .app
- ❌ Not the most modern looking (but functional)

**Alternative considered:** PyQt/PySide
- More modern appearance
- But: larger dependencies, more complex licensing

### Coordinate System
- macOS coordinate system: (0,0) = top-left of screen
- X increases → right
- Y increases → down
- Same as pyautogui default

### Building for macOS
**PyInstaller pros:**
- Simple, one command
- Cross-platform tool
- Good documentation

**py2app pros:**
- macOS-specific (better integration)
- More native .app structure
- Better code signing support

**Recommendation:** Start with PyInstaller, switch to py2app if needed

---

## ❓ Open Questions

1. **App Icon:** Do you want a custom icon, or use default Python icon?
2. **Error Handling:** How verbose should error messages be? Show technical details or keep simple?
3. **Countdown:** Keep 5-second countdown, or make it adjustable in GUI?
4. **Auto-open:** Should app automatically open output folder/PDF, or just show success message?

---

## 🎯 Next Steps

1. **Review this PRD** - Confirm scope and requirements
2. **Answer open questions** - Finalize any unclear decisions
3. **Begin Phase 1** - Start coding GUI implementation
4. **Iterative testing** - Test each phase as we build
5. **Final build** - Create standalone .app
6. **Documentation** - Update README for v2.0

---

**PRD Version:** 1.0  
**Created:** 2025-11-03  
**Author:** Claude (with adamartinik)  
**Status:** 📋 Ready for Review
