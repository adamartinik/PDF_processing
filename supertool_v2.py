#!/usr/bin/env python3
"""
PDF Screenshot Tool v2.0 (GUI)

Phase 1: Core GUI implementation with tabs and functional input fields.

Tabs:
- Screenshots
- PNG→PDF
- Complete Process

Features in Phase 1:
- Coordinate inputs (X1, Y1, X2, Y2) with default values
- Live preview of region dimensions (width × height)
- Progress bar placeholder
- Status message area
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import pyautogui
import threading
import time
import os
from PIL import Image


DEFAULT_X1 = 880
DEFAULT_Y1 = 180
DEFAULT_X2 = 1720
DEFAULT_Y2 = 1330


class PDFScreenshotToolGUI(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.master.title("PDF Screenshot Tool v2.0")
        self.master.geometry("900x650")
        self.master.minsize(860, 600)
        self._cancel_requested = False

        # Root layout
        self.pack(fill=tk.BOTH, expand=True)
        self._create_dark_glass_style()
        self._create_background()
        self._init_shared_vars()
        self._create_widgets()

    def _create_dark_glass_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Lighter palette for improved readability
        BG_COLOR = "#f4f5f7"
        CARD_BG = "#ffffff"
        PRIMARY = "#007AFF"
        PRIMARY_HOVER = "#2b89ff"
        TEXT_COLOR = "#1d1d1f"
        SECONDARY_TEXT = "#6b6b80"
        ENTRY_BG = "#ffffff"
        ENTRY_BORDER = "#d1d1d6"
        TROUGH = "#e8e8ed"

        # Window background
        try:
            self.master.configure(bg=BG_COLOR)
        except Exception:
            pass

        # Frames
        style.configure("TFrame", background=BG_COLOR)
        style.configure("Card.TFrame", background=CARD_BG, relief="flat")

        # Labels
        style.configure("Title.TLabel", background=CARD_BG, foreground=TEXT_COLOR, font=("Helvetica", 16, "bold"))
        style.configure("Heading.TLabel", background=CARD_BG, foreground=TEXT_COLOR, font=("Helvetica", 12, "bold"))
        style.configure("Body.TLabel", background=CARD_BG, foreground=TEXT_COLOR, font=("Helvetica", 11))
        style.configure("Status.TLabel", background=CARD_BG, foreground=SECONDARY_TEXT, font=("Helvetica", 10))

        # Labelframes
        style.configure("Section.TLabelframe", background=CARD_BG, padding=(16, 14))
        style.configure("Section.TLabelframe.Label", background=CARD_BG, foreground=TEXT_COLOR, font=("Helvetica", 12, "bold"))

        # Progressbar
        style.configure("Glass.Horizontal.TProgressbar", troughcolor=TROUGH, background=PRIMARY)

        # Notebook (tabs)
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        # Unselected tabs: normal padding; Selected: smaller top, larger bottom to appear raised
        style.configure("TNotebook.Tab", padding=(16, 10, 16, 14), background=CARD_BG, foreground=TEXT_COLOR, borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", CARD_BG)],
                  foreground=[("selected", TEXT_COLOR)],
                  relief=[("selected", "raised")],
                  padding=[("selected", (16, 4, 16, 18))])

        # Buttons
        style.configure("Primary.TButton", background=PRIMARY, foreground="#ffffff", padding=(12, 8))
        style.map("Primary.TButton",
                  background=[("active", PRIMARY_HOVER)])
        style.configure("Secondary.TButton", background="#e5e5ea", foreground=TEXT_COLOR, padding=(10, 6))
        style.map("Secondary.TButton",
                  background=[("active", "#efeff4")])

        # Entries (dark field background)
        style.configure("TEntry", fieldbackground=ENTRY_BG, foreground=TEXT_COLOR, bordercolor=ENTRY_BORDER, lightcolor=PRIMARY)
        style.map("TEntry",
                  fieldbackground=[("focus", ENTRY_BG)],
                  bordercolor=[("focus", PRIMARY)])

    def _create_background(self) -> None:
        # Disabled gradient background to fix black screen issue
        self._bg_canvas = None
        return

    def _redraw_background(self, event=None) -> None:
        c = self._bg_canvas
        if not c:
            return
        c.delete("all")
        w = c.winfo_width() or self.master.winfo_width()
        h = c.winfo_height() or self.master.winfo_height()
        # Draw vertical gradient (approximate glass gradient)
        start = (74, 144, 226)  # #4A90E2
        end = (139, 92, 246)    # #8B5CF6
        steps = max(1, int(h / 4))
        for i in range(steps):
            r = int(start[0] + (end[0] - start[0]) * i / steps)
            g = int(start[1] + (end[1] - start[1]) * i / steps)
            b = int(start[2] + (end[2] - start[2]) * i / steps)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y = int(i * (h / steps))
            c.create_rectangle(0, y, w, y + (h / steps) + 1, outline="", fill=color)
        # Subtle glass overlay
        c.create_rectangle(0, 0, w, h, fill="#000000", stipple="gray25", outline="")

    def _create_widgets(self) -> None:
        # Main container: overlay on background
        wrapper = ttk.Frame(self, style="TFrame")
        wrapper.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        notebook = ttk.Notebook(wrapper)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tabs (reordered: Complete, Screenshots Only, PNG→PDF)
        self.tab_complete = ttk.Frame(notebook)
        self.tab_screenshots = ttk.Frame(notebook)
        self.tab_png_to_pdf = ttk.Frame(notebook)

        notebook.add(self.tab_complete, text="🚀 Complete Process")
        notebook.add(self.tab_screenshots, text="📸 Screenshots Only")
        notebook.add(self.tab_png_to_pdf, text="📄 PNG → PDF")

        # Build individual tabs
        self._build_tab_complete(self.tab_complete)
        self._build_tab_screenshots(self.tab_screenshots)
        self._build_tab_png_to_pdf(self.tab_png_to_pdf)

    def _init_shared_vars(self) -> None:
        # Shared variables used across tabs
        self.var_x1 = tk.StringVar(value=str(DEFAULT_X1))
        self.var_y1 = tk.StringVar(value=str(DEFAULT_Y1))
        self.var_x2 = tk.StringVar(value=str(DEFAULT_X2))
        self.var_y2 = tk.StringVar(value=str(DEFAULT_Y2))
        self.var_num_pages = tk.StringVar(value="")
        self.var_output_folder = tk.StringVar(value="")

    # ---------------------- Screenshots Tab ----------------------
    def _build_tab_screenshots(self, parent: ttk.Frame) -> None:
        container = ttk.Frame(parent, padding=(12, 12))
        container.pack(fill=tk.BOTH, expand=True)

        # Coordinates group
        coords_frame = ttk.Labelframe(container, text="Screenshot Region Settings", style="Section.TLabelframe")
        coords_frame.pack(fill=tk.X, expand=False, pady=(0, 12))

        # Top row: Top-Left
        row1 = ttk.Frame(coords_frame, style="Card.TFrame")
        row1.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row1, text="Top-Left (X1, Y1):").pack(side=tk.LEFT)
        self.entry_x1 = ttk.Entry(row1, width=8, textvariable=self.var_x1)
        self.entry_x1.pack(side=tk.LEFT, padx=(8, 12))
        self.entry_y1 = ttk.Entry(row1, width=8, textvariable=self.var_y1)
        self.entry_y1.pack(side=tk.LEFT, padx=(0, 12))

        # Second row: Bottom-Right
        row2 = ttk.Frame(coords_frame, style="Card.TFrame")
        row2.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row2, text="Bottom-Right (X2, Y2):").pack(side=tk.LEFT)
        self.entry_x2 = ttk.Entry(row2, width=8, textvariable=self.var_x2)
        self.entry_x2.pack(side=tk.LEFT, padx=(8, 12))
        self.entry_y2 = ttk.Entry(row2, width=8, textvariable=self.var_y2)
        self.entry_y2.pack(side=tk.LEFT, padx=(0, 12))

        # Third row: Live preview (width × height)
        row3 = ttk.Frame(coords_frame, style="Card.TFrame")
        row3.pack(fill=tk.X, padx=4, pady=(6, 4))
        self.label_region_preview = ttk.Label(row3, text=self._compute_region_preview(), style="Status.TLabel")
        self.label_region_preview.pack(side=tk.LEFT)

        # Bind value changes for live preview
        for var in (self.var_x1, self.var_y1, self.var_x2, self.var_y2):
            var.trace_add("write", lambda *_: self._update_region_preview())

        # Processing settings
        process_frame = ttk.Labelframe(container, text="PDF Processing", style="Section.TLabelframe")
        process_frame.pack(fill=tk.X, expand=False)

        row4 = ttk.Frame(process_frame, style="Card.TFrame")
        row4.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row4, text="Number of pages:").pack(side=tk.LEFT)
        self.entry_num_pages = ttk.Entry(row4, width=10, textvariable=self.var_num_pages)
        self.entry_num_pages.pack(side=tk.LEFT, padx=(8, 12))

        row5 = ttk.Frame(process_frame, style="Card.TFrame")
        row5.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row5, text="Output folder name:").pack(side=tk.LEFT)
        self.entry_output_folder = ttk.Entry(row5, width=32, textvariable=self.var_output_folder)
        self.entry_output_folder.pack(side=tk.LEFT, padx=(8, 12))

        # Actions
        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(16, 10))
        self.btn_test_region = ttk.Button(actions, text="Test Region", command=self._on_test_region, style="Secondary.TButton")
        self.btn_test_region.pack(side=tk.LEFT)
        ttk.Label(actions, text="  ").pack(side=tk.LEFT)  # spacer
        self.btn_start = ttk.Button(actions, text="Start Screenshots", command=self._on_start_screenshots, style="Primary.TButton")
        self.btn_start.pack(side=tk.LEFT)
        ttk.Label(actions, text="  ").pack(side=tk.LEFT)
        self.btn_cancel = ttk.Button(actions, text="Cancel", command=self._on_cancel_screenshots, style="Secondary.TButton")
        self.btn_cancel.pack(side=tk.LEFT)

        # Progress + Status
        bottom = ttk.Frame(container)
        bottom.pack(fill=tk.X, side=tk.BOTTOM, pady=(8, 0))
        self.progress = ttk.Progressbar(bottom, mode="determinate", style="Glass.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, padx=2)
        self.status_var = tk.StringVar(value="Status: Ready")
        self.status_label = ttk.Label(bottom, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(anchor=tk.W, padx=2, pady=(6, 0))

    # ---------------------- PNG→PDF Tab ----------------------
    def _build_tab_png_to_pdf(self, parent: ttk.Frame) -> None:
        container = ttk.Frame(parent, padding=(12, 12))
        container.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(container, text="PNG → PDF", style="Title.TLabel")
        title.pack(anchor=tk.W, pady=(0, 8))

        # Placeholder UI elements for Phase 1
        row = ttk.Frame(container)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Folder with PNG files:" ).pack(side=tk.LEFT)
        self.var_png_folder = tk.StringVar(value="")
        self.entry_png_folder = ttk.Entry(row, width=48, textvariable=self.var_png_folder)
        self.entry_png_folder.pack(side=tk.LEFT, padx=(8, 8))
        ttk.Button(row, text="Browse", command=self._on_browse_png_folder).pack(side=tk.LEFT)

        row2 = ttk.Frame(container)
        row2.pack(fill=tk.X, pady=4)
        ttk.Label(row2, text="Output PDF name:" ).pack(side=tk.LEFT)
        self.var_pdf_name = tk.StringVar(value="")
        self.entry_pdf_name = ttk.Entry(row2, width=32, textvariable=self.var_pdf_name)
        self.entry_pdf_name.pack(side=tk.LEFT, padx=(8, 8))

        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(8, 6))
        self.btn_create_pdf = ttk.Button(actions, text="Create PDF", command=self._on_create_pdf, style="Primary.TButton")
        self.btn_create_pdf.pack(side=tk.LEFT)
        ttk.Label(actions, text="  ").pack(side=tk.LEFT)
        self.btn_open_pdf = ttk.Button(actions, text="Open PDF", command=self._on_open_pdf, state=tk.DISABLED, style="Secondary.TButton")
        self.btn_open_pdf.pack(side=tk.LEFT)

        bottom = ttk.Frame(container)
        bottom.pack(fill=tk.X, side=tk.BOTTOM, pady=(8, 0))
        self.progress_png = ttk.Progressbar(bottom, mode="determinate", style="Blue.Horizontal.TProgressbar")
        self.progress_png.pack(fill=tk.X, padx=2)
        self.status_var_png = tk.StringVar(value="Status: Ready")
        ttk.Label(bottom, textvariable=self.status_var_png, style="Status.TLabel").pack(anchor=tk.W, padx=2, pady=(6, 0))
        self._last_pdf_path = None

    # ---------------------- Complete Process Tab ----------------------
    def _build_tab_complete(self, parent: ttk.Frame) -> None:
        container = ttk.Frame(parent, padding=(16, 16))
        container.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(container, text="Complete Process", style="Title.TLabel")
        title.pack(anchor=tk.W, pady=(0, 12))

        # Region settings (same variables)
        coords_frame = ttk.Labelframe(container, text="Screenshot Region Settings", style="Section.TLabelframe")
        coords_frame.pack(fill=tk.X, expand=False, pady=(0, 12))

        row1 = ttk.Frame(coords_frame, style="Card.TFrame")
        row1.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row1, text="Top-Left (X1, Y1):").pack(side=tk.LEFT)
        ttk.Entry(row1, width=8, textvariable=self.var_x1).pack(side=tk.LEFT, padx=(8, 12))
        ttk.Entry(row1, width=8, textvariable=self.var_y1).pack(side=tk.LEFT, padx=(0, 12))

        row2 = ttk.Frame(coords_frame, style="Card.TFrame")
        row2.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row2, text="Bottom-Right (X2, Y2):").pack(side=tk.LEFT)
        ttk.Entry(row2, width=8, textvariable=self.var_x2).pack(side=tk.LEFT, padx=(8, 12))
        ttk.Entry(row2, width=8, textvariable=self.var_y2).pack(side=tk.LEFT, padx=(0, 12))

        row3 = ttk.Frame(coords_frame, style="Card.TFrame")
        row3.pack(fill=tk.X, padx=4, pady=(6, 4))
        self.label_region_preview_complete = ttk.Label(row3, text=self._compute_region_preview(), style="Status.TLabel")
        self.label_region_preview_complete.pack(side=tk.LEFT)
        # Bind changes
        for var in (self.var_x1, self.var_y1, self.var_x2, self.var_y2):
            var.trace_add("write", lambda *_: self._update_region_preview_complete())

        # Processing settings
        process_frame = ttk.Labelframe(container, text="PDF Processing", style="Section.TLabelframe")
        process_frame.pack(fill=tk.X, expand=False)

        row4 = ttk.Frame(process_frame, style="Card.TFrame")
        row4.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row4, text="Number of pages:").pack(side=tk.LEFT)
        ttk.Entry(row4, width=10, textvariable=self.var_num_pages).pack(side=tk.LEFT, padx=(8, 12))

        row5 = ttk.Frame(process_frame, style="Card.TFrame")
        row5.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(row5, text="Output folder name:").pack(side=tk.LEFT)
        ttk.Entry(row5, width=32, textvariable=self.var_output_folder).pack(side=tk.LEFT, padx=(8, 12))

        # Delete PNGs option
        self.var_delete_pngs = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            container,
            text="Delete PNG files after PDF creation",
            variable=self.var_delete_pngs
        ).pack(anchor=tk.W, pady=(12, 6))

        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(12, 8))
        self.btn_test_region_complete = ttk.Button(actions, text="Test Region", command=self._on_test_region_complete, style="Secondary.TButton")
        self.btn_test_region_complete.pack(side=tk.LEFT)
        ttk.Label(actions, text="  ").pack(side=tk.LEFT)
        self.btn_start_complete = ttk.Button(actions, text="Start Complete Process", command=self._on_start_complete, style="Primary.TButton")
        self.btn_start_complete.pack(side=tk.LEFT)
        ttk.Label(actions, text="  ").pack(side=tk.LEFT)
        self.btn_open_pdf_complete = ttk.Button(actions, text="Open PDF", command=self._on_open_pdf, state=tk.DISABLED, style="Secondary.TButton")
        self.btn_open_pdf_complete.pack(side=tk.LEFT)
        ttk.Label(actions, text="  ").pack(side=tk.LEFT)
        self.btn_open_folder_complete = ttk.Button(actions, text="Open Folder", command=self._on_open_complete_folder, state=tk.DISABLED, style="Secondary.TButton")
        self.btn_open_folder_complete.pack(side=tk.LEFT)

        bottom = ttk.Frame(container)
        bottom.pack(fill=tk.X, side=tk.BOTTOM, pady=(8, 0))
        self.progress_complete = ttk.Progressbar(bottom, mode="determinate", style="Blue.Horizontal.TProgressbar")
        self.progress_complete.pack(fill=tk.X, padx=2)
        self.status_var_complete = tk.StringVar(value="Status: Ready")
        ttk.Label(bottom, textvariable=self.status_var_complete, style="Status.TLabel").pack(anchor=tk.W, padx=2, pady=(6, 0))

    # ---------------------- Helpers ----------------------
    def _compute_region_preview(self) -> str:
        x1, y1, x2, y2 = self._safe_int(self.var_x1), self._safe_int(self.var_y1), self._safe_int(self.var_x2), self._safe_int(self.var_y2)
        width = max(0, x2 - x1)
        height = max(0, y2 - y1)
        return f"→ Region: {width}×{height} pixels"

    def _update_region_preview(self) -> None:
        self.label_region_preview.configure(text=self._compute_region_preview())

    def _update_region_preview_complete(self) -> None:
        if hasattr(self, 'label_region_preview_complete'):
            self.label_region_preview_complete.configure(text=self._compute_region_preview())

    @staticmethod
    def _safe_int(var: tk.StringVar) -> int:
        try:
            return int(var.get())
        except (TypeError, ValueError):
            return 0

    def _update_status(self, message: str) -> None:
        self.status_var.set(message)
        self.master.update_idletasks()

    def _update_progress(self, value: float) -> None:
        try:
            self.progress["value"] = float(value)
        except Exception:
            self.progress["value"] = 0
        self.master.update_idletasks()

    # ---------------------- Event Handlers (Placeholders) ----------------------
    def _test_region_common(self) -> str:
        try:
            x1 = int(self.var_x1.get())
            y1 = int(self.var_y1.get())
            x2 = int(self.var_x2.get())
            y2 = int(self.var_y2.get())
        except (TypeError, ValueError):
            return "Status: Invalid coordinates (must be integers)"

        x = x1
        y = y1
        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            return "Status: Invalid region (X2>X1 and Y2>Y1 required)"

        try:
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            desktop = Path.home() / "Desktop"
            out_path = desktop / "test_region.png"
            screenshot.save(str(out_path))
            return "Status: Test screenshot saved to Desktop/test_region.png"
        except Exception as e:
            return f"Status: Screenshot failed: {e}"

    def _on_test_region(self) -> None:
        message = self._test_region_common()
        self.status_var.set(message)

    def _on_test_region_complete(self) -> None:
        message = self._test_region_common()
        self.status_var_complete.set(message)

    def _on_start_screenshots(self) -> None:
        # Disable controls and start background processing
        self._cancel_requested = False
        self.btn_start.configure(state=tk.DISABLED)
        self.btn_test_region.configure(state=tk.DISABLED)
        self.btn_cancel.configure(state=tk.NORMAL)
        self._update_progress(0)
        self._update_status("Status: Preparing...")

        thread = threading.Thread(target=self._do_screenshot_pdf, daemon=True)
        thread.start()

    def _on_cancel_screenshots(self) -> None:
        # Set cancel flag; loop checks this flag
        self._cancel_requested = True
        self._update_status("Status: Cancel requested")

    def _on_browse_png_folder(self) -> None:
        folder = filedialog.askdirectory(
            title="Select folder with PNG files",
            initialdir=str(Path.home() / "Desktop")
        )
        if not folder:
            return
        self.var_png_folder.set(folder)
        try:
            count = len(sorted(Path(folder).glob("*.png")))
        except Exception:
            count = 0
        self.status_var_png.set(f"Status: Found {count} PNG files")
        # Suggest default PDF name
        folder_name = Path(folder).name
        suggested = f"{folder_name}.pdf"
        self.var_pdf_name.set(suggested)

    def _on_create_pdf(self) -> None:
        # Validate selection
        png_folder = (self.var_png_folder.get() or "").strip()
        if not png_folder:
            self.status_var_png.set("Status: Select a PNG folder first")
            return
        # Disable controls and start background job
        self.btn_create_pdf.configure(state=tk.DISABLED)
        self.btn_open_pdf.configure(state=tk.DISABLED)
        self.progress_png["value"] = 0
        self.status_var_png.set("Status: Preparing...")
        thread = threading.Thread(target=self._do_png_to_pdf, daemon=True)
        thread.start()

    def _on_start_complete(self) -> None:
        # Validate that required inputs exist on Screenshots tab
        try:
            int(self.var_x1.get()); int(self.var_y1.get()); int(self.var_x2.get()); int(self.var_y2.get())
            int(self.var_num_pages.get())
        except Exception:
            self.status_var_complete.set("Status: Invalid inputs (check coordinates and page count)")
            return
        # Disable controls and start thread
        self.btn_start_complete.configure(state=tk.DISABLED)
        self.btn_open_pdf_complete.configure(state=tk.DISABLED)
        self.btn_open_folder_complete.configure(state=tk.DISABLED)
        self.progress_complete["value"] = 0
        self.status_var_complete.set("Status: Preparing...")
        thread = threading.Thread(target=self._do_complete_process, daemon=True)
        thread.start()

    # ---------------------- Complete Process ----------------------
    def _do_complete_process(self) -> None:
        start_time = time.time()
        try:
            # Read and validate shared inputs from Screenshots tab
            try:
                x1 = int(self.var_x1.get())
                y1 = int(self.var_y1.get())
                x2 = int(self.var_x2.get())
                y2 = int(self.var_y2.get())
                num_pages = int(self.var_num_pages.get())
            except (TypeError, ValueError):
                self.status_var_complete.set("Status: Invalid inputs (coordinates/pages)")
                return

            output_folder_name = (self.var_output_folder.get() or "PDF_Screenshots").strip()
            if not output_folder_name:
                self.status_var_complete.set("Status: Output folder name is required")
                return

            # Compute region
            x = x1; y = y1
            width = x2 - x1; height = y2 - y1
            if width <= 0 or height <= 0 or num_pages <= 0:
                self.status_var_complete.set("Status: Invalid region or page count")
                return

            # Phase 1: Screenshots (0-50%)
            self.status_var_complete.set("Status: Phase 1/2: Taking screenshots...")
            self.master.update_idletasks()

            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1

            desktop_path = Path.home() / "Desktop"
            folder_path = desktop_path / output_folder_name
            folder_path.mkdir(exist_ok=True)

            for i in range(5, 0, -1):
                self.status_var_complete.set(f"Status: Starting in {i}...")
                self.master.update_idletasks()
                time.sleep(1)

            for page in range(1, num_pages + 1):
                self.status_var_complete.set(f"Status: Processing page {page}/{num_pages}")
                self.progress_complete["value"] = ((page - 1) / max(1, num_pages)) * 50.0
                self.master.update_idletasks()

                filename = f"strana_{page:02d}.png"
                out_path = folder_path / filename
                shot = pyautogui.screenshot(region=(x, y, width, height))
                shot.save(str(out_path))
                pyautogui.press('down')
                time.sleep(0.5)

            self.status_var_complete.set("Status: Phase 1/2: ✅ Screenshots complete")
            self.master.update_idletasks()
            time.sleep(1)

            # Phase 2: PNG → PDF (50-100%)
            self.status_var_complete.set("Status: Phase 2/2: Converting to PDF...")
            self.master.update_idletasks()

            png_files = sorted(folder_path.glob("*.png"))
            if not png_files:
                self.status_var_complete.set("Status: No PNG files found after screenshots")
                return

            images = []
            total = len(png_files)
            for i, png_file in enumerate(png_files):
                self.progress_complete["value"] = 50.0 + (i / max(1, total)) * 25.0  # 50 → 75
                self.status_var_complete.set(f"Status: Loading {png_file.name} ({i+1}/{total})")
                self.master.update_idletasks()
                img = Image.open(png_file)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)

            pdf_name = f"{output_folder_name}.pdf"
            pdf_path = folder_path / pdf_name
            self.status_var_complete.set(f"Status: Creating PDF: {pdf_name}")
            self.progress_complete["value"] = 90.0
            self.master.update_idletasks()

            first_image = images[0]
            other_images = images[1:] if len(images) > 1 else None
            if other_images:
                first_image.save(
                    pdf_path,
                    format='PDF',
                    append_images=other_images,
                    save_all=True,
                    quality=95,
                    optimize=False
                )
            else:
                first_image.save(pdf_path, format='PDF', quality=95)

            # Optionally delete PNGs
            deleted = 0
            if self.var_delete_pngs.get():
                for f in png_files:
                    try:
                        f.unlink()
                        deleted += 1
                    except Exception:
                        pass

            # Finish
            self.progress_complete["value"] = 100.0
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            if self.var_delete_pngs.get():
                self.status_var_complete.set(f"Status: ✅ Complete! PDF created, {deleted} PNG files deleted")
            else:
                self.status_var_complete.set("Status: Process complete! PDF created.")
            self._last_pdf_path = str(pdf_path)
            self._complete_last_folder = str(folder_path)
        except Exception as e:
            self.status_var_complete.set(f"Status: Error in complete process: {e}")
        finally:
            # Re-enable controls and enable open buttons if available
            try:
                self.btn_start_complete.configure(state=tk.NORMAL)
                if getattr(self, '_last_pdf_path', None) and Path(self._last_pdf_path).exists():
                    self.btn_open_pdf_complete.configure(state=tk.NORMAL)
                if getattr(self, '_complete_last_folder', None) and Path(self._complete_last_folder).exists():
                    self.btn_open_folder_complete.configure(state=tk.NORMAL)
            except Exception:
                pass

    def _on_open_complete_folder(self) -> None:
        if getattr(self, '_complete_last_folder', None) and Path(self._complete_last_folder).exists():
            os.system(f'open "{self._complete_last_folder}"')

    # ---------------------- PNG→PDF Processing ----------------------
    def _do_png_to_pdf(self) -> None:
        try:
            png_folder_path = (self.var_png_folder.get() or "").strip()
            pdf_name = (self.var_pdf_name.get() or "").strip()
            if not png_folder_path:
                self.status_var_png.set("Status: PNG folder is required")
                return
            if not pdf_name:
                self.status_var_png.set("Status: Output PDF name is required")
                return

            folder_path = Path(png_folder_path)
            png_files = sorted(folder_path.glob("*.png"))
            if not png_files:
                self.status_var_png.set("Status: No PNG files found!")
                return

            self.status_var_png.set(f"Status: Processing {len(png_files)} images...")

            images = []
            total = len(png_files)
            for i, png_file in enumerate(png_files):
                self.progress_png["value"] = (i / max(1, total)) * 50.0
                self.status_var_png.set(f"Status: Loading {png_file.name} ({i+1}/{total})")
                self.master.update_idletasks()
                img = Image.open(png_file)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)

            # Prepare output path
            if not pdf_name.lower().endswith('.pdf'):
                pdf_name = f"{pdf_name}.pdf"
            pdf_path = folder_path / pdf_name

            self.status_var_png.set(f"Status: Creating PDF: {pdf_name}")
            self.progress_png["value"] = 75.0
            self.master.update_idletasks()

            first_image = images[0]
            other_images = images[1:] if len(images) > 1 else None
            if other_images:
                first_image.save(
                    pdf_path,
                    format='PDF',
                    append_images=other_images,
                    save_all=True,
                    quality=95,
                    optimize=False
                )
            else:
                first_image.save(pdf_path, format='PDF', quality=95)

            # Done
            self.progress_png["value"] = 100.0
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            self.status_var_png.set(f"Status: ✅ PDF created! {pdf_path.name} ({size_mb:.1f} MB, {len(images)} pages)")
            self._last_pdf_path = str(pdf_path)
        except Exception as e:
            self.status_var_png.set(f"Status: Error creating PDF: {e}")
        finally:
            try:
                # Close images to free memory
                for img in locals().get('images', []):
                    try:
                        img.close()
                    except Exception:
                        pass
                self.btn_create_pdf.configure(state=tk.NORMAL)
                # Enable open button if we have a PDF
                if self._last_pdf_path and Path(self._last_pdf_path).exists():
                    self.btn_open_pdf.configure(state=tk.NORMAL)
            except Exception:
                pass

    def _on_open_pdf(self) -> None:
        if self._last_pdf_path and Path(self._last_pdf_path).exists():
            os.system(f'open "{self._last_pdf_path}"')

    # ---------------------- Screenshots Processing ----------------------
    def _do_screenshot_pdf(self) -> None:
        try:
            # Safety settings
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1

            # Read and validate inputs
            try:
                x1 = int(self.var_x1.get())
                y1 = int(self.var_y1.get())
                x2 = int(self.var_x2.get())
                y2 = int(self.var_y2.get())
            except (TypeError, ValueError):
                self._update_status("Status: Invalid coordinates (integers required)")
                return

            try:
                num_pages = int(self.var_num_pages.get())
            except (TypeError, ValueError):
                self._update_status("Status: Invalid number of pages")
                return

            output_folder_name = (self.var_output_folder.get() or "PDF_Screenshots").strip()
            if not output_folder_name:
                self._update_status("Status: Output folder name is required")
                return

            # Compute region
            x = x1
            y = y1
            width = x2 - x1
            height = y2 - y1

            if width <= 0 or height <= 0 or num_pages <= 0:
                self._update_status("Status: Invalid inputs (check coordinates and page count)")
                return

            # Create folder on Desktop
            desktop_path = Path.home() / "Desktop"
            folder_path = desktop_path / output_folder_name
            folder_path.mkdir(exist_ok=True)

            # Countdown
            for i in range(5, 0, -1):
                if self._cancel_requested:
                    self._update_status("Status: Cancelled before start")
                    self._update_progress(0)
                    return
                self._update_status(f"Starting in {i}...")
                time.sleep(1)

            # Main loop
            for page in range(1, num_pages + 1):
                if self._cancel_requested:
                    self._update_status("Status: Cancelled")
                    break

                self._update_status(f"Processing page {page}/{num_pages}")
                progress_value = (page - 1) / max(1, num_pages) * 100.0
                self._update_progress(progress_value)

                filename = f"strana_{page:02d}.png"
                out_path = folder_path / filename

                # Take screenshot
                shot = pyautogui.screenshot(region=(x, y, width, height))
                shot.save(str(out_path))

                # Next page
                pyautogui.press('down')
                time.sleep(0.5)

            if not self._cancel_requested:
                self._update_progress(100.0)
                self._update_status(f"✅ Done! {num_pages} screenshots saved to {output_folder_name}")
        except Exception as e:
            self._update_status(f"Status: Error during screenshots: {e}")
        finally:
            # Re-enable controls
            try:
                self.btn_start.configure(state=tk.NORMAL)
                self.btn_test_region.configure(state=tk.NORMAL)
                self.btn_cancel.configure(state=tk.DISABLED)
            except Exception:
                pass


def main() -> None:
    root = tk.Tk()
    # Ensure ttk widgets scale with DPI
    try:
        from ctypes import windll  # noqa: F401
        # If available, skip; macOS usually handles DPI automatically
    except Exception:
        pass
    PDFScreenshotToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


