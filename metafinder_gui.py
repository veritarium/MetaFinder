#!/usr/bin/env python3
"""
MetaFinder GUI
Modern interface for file metadata extraction and filtering
"""

import sys
import os
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import customtkinter as ctk
from tkinter import filedialog, messagebox

from metafinder import MetadataScanner, DatabaseManager
from metafinder.scanner import check_requirements


# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MetaFinderGUI(ctk.CTk):
    """Main GUI application for MetaFinder"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("MetaFinder - Universal File Metadata Search")
        self.geometry("1400x900")
        self.minsize(1200, 700)

        # State
        self.db: Optional[DatabaseManager] = None
        self.scanner: Optional[MetadataScanner] = None
        self.current_results: List[Dict[str, Any]] = []
        self.scanning = False

        # Check requirements
        if not self._check_requirements():
            return

        # Initialize components
        self._init_database()
        self._create_layout()
        self._load_initial_data()

    def _check_requirements(self) -> bool:
        """Check if all requirements are met"""
        reqs = check_requirements()

        if not reqs['pyexiftool']:
            messagebox.showerror(
                "Missing Dependency",
                "PyExifTool is not installed.\n\n"
                "Install with: pip install pyexiftool"
            )
            self.destroy()
            return False

        if not reqs['exiftool_binary']:
            response = messagebox.askyesno(
                "ExifTool Not Found",
                "ExifTool binary is not installed.\n\n"
                "MetaFinder requires ExifTool to extract metadata.\n\n"
                "Install instructions:\n"
                "  • macOS: brew install exiftool\n"
                "  • Linux: sudo apt install libimage-exiftool-perl\n"
                "  • Windows: Download from exiftool.org\n\n"
                "Continue anyway? (Some features won't work)"
            )
            if not response:
                self.destroy()
                return False

        return True

    def _init_database(self):
        """Initialize database connection"""
        db_path = "data/metafinder.db"
        self.db = DatabaseManager(db_path)
        self.scanner = MetadataScanner(self.db)

    def _create_layout(self):
        """Create the main layout"""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top bar
        self._create_top_bar()

        # Left sidebar (filters)
        self._create_filter_panel()

        # Center panel (results)
        self._create_results_panel()

        # Bottom status bar
        self._create_status_bar()

    def _create_top_bar(self):
        """Create top bar with scan button and controls"""
        top_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            top_frame,
            text="📁 MetaFinder",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Scan button
        self.scan_button = ctk.CTkButton(
            top_frame,
            text="🔍 Scan Folder",
            command=self._scan_folder,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.scan_button.grid(row=0, column=2, padx=20, pady=20)

        # Stats button
        stats_button = ctk.CTkButton(
            top_frame,
            text="📊 Statistics",
            command=self._show_statistics,
            width=120,
            height=40
        )
        stats_button.grid(row=0, column=3, padx=(0, 20), pady=20)

    def _create_filter_panel(self):
        """Create left sidebar with filters"""
        filter_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        filter_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        filter_frame.grid_rowconfigure(6, weight=1)

        # Title
        filter_title = ctk.CTkLabel(
            filter_frame,
            text="🔍 Filters",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        filter_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Quick search
        ctk.CTkLabel(filter_frame, text="Quick Search:", anchor="w").grid(
            row=1, column=0, padx=20, pady=(10, 5), sticky="w"
        )
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Search files..."
        )
        self.search_entry.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self._apply_filters())

        # File Type filter
        ctk.CTkLabel(filter_frame, text="File Type:", anchor="w").grid(
            row=3, column=0, padx=20, pady=(10, 5), sticky="w"
        )
        self.type_var = ctk.StringVar(value="All")
        self.type_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "image", "document", "audio", "video", "archive", "code"],
            variable=self.type_var,
            command=lambda _: self._apply_filters()
        )
        self.type_menu.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Extension filter
        ctk.CTkLabel(filter_frame, text="Extension:", anchor="w").grid(
            row=5, column=0, padx=20, pady=(10, 5), sticky="w"
        )
        self.extension_var = ctk.StringVar(value="All")
        self.extension_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["All"],
            variable=self.extension_var,
            command=lambda _: self._apply_filters()
        )
        self.extension_menu.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Author filter
        ctk.CTkLabel(filter_frame, text="Author:", anchor="w").grid(
            row=7, column=0, padx=20, pady=(10, 5), sticky="w"
        )
        self.author_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Filter by author..."
        )
        self.author_entry.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.author_entry.bind("<Return>", lambda e: self._apply_filters())

        # Camera filter
        ctk.CTkLabel(filter_frame, text="Camera:", anchor="w").grid(
            row=9, column=0, padx=20, pady=(10, 5), sticky="w"
        )
        self.camera_var = ctk.StringVar(value="All")
        self.camera_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["All"],
            variable=self.camera_var,
            command=lambda _: self._apply_filters()
        )
        self.camera_menu.grid(row=10, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Apply filters button
        apply_button = ctk.CTkButton(
            filter_frame,
            text="Apply Filters",
            command=self._apply_filters,
            fg_color="#2B8A3E",
            hover_color="#37A946"
        )
        apply_button.grid(row=11, column=0, padx=20, pady=20, sticky="ew")

        # Clear filters button
        clear_button = ctk.CTkButton(
            filter_frame,
            text="Clear All",
            command=self._clear_filters,
            fg_color="#666666",
            hover_color="#777777"
        )
        clear_button.grid(row=12, column=0, padx=20, pady=(0, 20), sticky="ew")

    def _create_results_panel(self):
        """Create center panel for results"""
        results_frame = ctk.CTkFrame(self, corner_radius=0)
        results_frame.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        # Results header
        header_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)

        self.results_label = ctk.CTkLabel(
            header_frame,
            text="📄 Results (0 files)",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        self.results_label.grid(row=0, column=0, sticky="w")

        # Scrollable results area
        self.results_scroll = ctk.CTkScrollableFrame(
            results_frame,
            fg_color="transparent"
        )
        self.results_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.results_scroll.grid_columnconfigure(0, weight=1)

        # Welcome message
        self._show_welcome_message()

    def _create_status_bar(self):
        """Create bottom status bar"""
        status_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to scan files",
            anchor="w"
        )
        self.status_label.pack(side="left", padx=20, pady=10)

    def _show_welcome_message(self):
        """Show welcome message when no files"""
        welcome_frame = ctk.CTkFrame(self.results_scroll)
        welcome_frame.grid(row=0, column=0, sticky="ew", pady=100)

        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="👋 Welcome to MetaFinder!",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome_label.pack(pady=(40, 20))

        info_label = ctk.CTkLabel(
            welcome_frame,
            text="Click 'Scan Folder' to start extracting file metadata\n\n"
                 "MetaFinder will analyze your files and let you search by:\n"
                 "• File type and extension\n"
                 "• Author and title\n"
                 "• Camera make and model\n"
                 "• Date taken\n"
                 "• And much more!",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        info_label.pack(pady=20)

        scan_welcome_button = ctk.CTkButton(
            welcome_frame,
            text="🔍 Scan Your First Folder",
            command=self._scan_folder,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        scan_welcome_button.pack(pady=40)

    def _load_initial_data(self):
        """Load initial data and populate filters"""
        # Load existing files if any
        stats = self.db.get_statistics()

        if stats['total_files'] > 0:
            self._update_status(f"Database loaded: {stats['total_files']} files")
            self._populate_filters()
            self._apply_filters()
        else:
            self._update_status("No files in database. Click 'Scan Folder' to start.")

    def _populate_filters(self):
        """Populate filter dropdowns with available values"""
        # Get unique extensions
        extensions = self.db.get_unique_values('extension', limit=50)
        if extensions:
            self.extension_menu.configure(values=["All"] + extensions)

        # Get unique camera makes
        cameras = self.db.get_unique_values('camera_make', limit=30)
        if cameras:
            self.camera_menu.configure(values=["All"] + cameras)

    def _scan_folder(self):
        """Open folder dialog and scan"""
        if self.scanning:
            messagebox.showwarning("Scan in Progress", "A scan is already running. Please wait.")
            return

        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if not folder:
            return

        # Confirm scan
        response = messagebox.askyesno(
            "Start Scan",
            f"Scan all files in:\n{folder}\n\nThis may take several minutes for large folders."
        )

        if not response:
            return

        # Start scan in background thread
        self.scanning = True
        self.scan_button.configure(state="disabled", text="⏳ Scanning...")
        self._update_status("Starting scan...")

        thread = threading.Thread(target=self._scan_folder_thread, args=(folder,))
        thread.daemon = True
        thread.start()

    def _scan_folder_thread(self, folder: str):
        """Scan folder in background thread"""
        try:
            def progress_callback(current, total, filename):
                percent = (current / total) * 100
                self.after(0, lambda: self._update_status(
                    f"Scanning: {current}/{total} ({percent:.1f}%) - {filename[:50]}"
                ))

            stats = self.scanner.scan_folder(
                folder,
                recursive=True,
                progress_callback=progress_callback
            )

            # Update UI on completion
            self.after(0, lambda: self._scan_complete(stats))

        except Exception as e:
            self.after(0, lambda: self._scan_error(str(e)))

    def _scan_complete(self, stats: Dict[str, Any]):
        """Handle scan completion"""
        self.scanning = False
        self.scan_button.configure(state="normal", text="🔍 Scan Folder")

        messagebox.showinfo(
            "Scan Complete",
            f"Successfully scanned {stats['scanned']}/{stats['total']} files\n"
            f"Success rate: {stats['success_rate']:.1f}%"
        )

        self._update_status(f"Scan complete: {stats['scanned']} files indexed")
        self._populate_filters()
        self._apply_filters()

    def _scan_error(self, error: str):
        """Handle scan error"""
        self.scanning = False
        self.scan_button.configure(state="normal", text="🔍 Scan Folder")

        messagebox.showerror("Scan Error", f"Error during scan:\n{error}")
        self._update_status("Scan failed")

    def _apply_filters(self):
        """Apply current filters and update results"""
        # Build search parameters
        search_params = {'limit': 100}

        if self.type_var.get() != "All":
            search_params['file_type'] = self.type_var.get()

        if self.extension_var.get() != "All":
            search_params['extension'] = self.extension_var.get()

        author = self.author_entry.get().strip()
        if author:
            search_params['author'] = author

        if self.camera_var.get() != "All":
            search_params['camera_make'] = self.camera_var.get()

        # Search
        self.current_results = self.db.search_files(**search_params)

        # Update display
        self._display_results()

    def _clear_filters(self):
        """Clear all filters"""
        self.type_var.set("All")
        self.extension_var.set("All")
        self.camera_var.set("All")
        self.author_entry.delete(0, 'end')
        self.search_entry.delete(0, 'end')
        self._apply_filters()

    def _display_results(self):
        """Display search results"""
        # Clear existing results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()

        # Update count
        count = len(self.current_results)
        self.results_label.configure(text=f"📄 Results ({count} files)")

        if count == 0:
            # No results message
            no_results = ctk.CTkLabel(
                self.results_scroll,
                text="No files found matching your filters",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_results.grid(row=0, column=0, pady=100)
            return

        # Display results
        for i, record in enumerate(self.current_results):
            self._create_result_card(record, i)

    def _create_result_card(self, record: Dict[str, Any], row: int):
        """Create a result card for a file"""
        card = ctk.CTkFrame(self.results_scroll)
        card.grid(row=row, column=0, sticky="ew", pady=5)
        card.grid_columnconfigure(1, weight=1)

        # Icon based on type
        icon_map = {
            'image': '🖼️',
            'document': '📄',
            'audio': '🎵',
            'video': '🎬',
            'archive': '📦',
            'code': '💻',
            'unknown': '📁'
        }
        icon = icon_map.get(record['file_type'], '📁')

        # Icon
        icon_label = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=32))
        icon_label.grid(row=0, column=0, rowspan=3, padx=20, pady=10)

        # Filename
        name_label = ctk.CTkLabel(
            card,
            text=record['name'],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))

        # Metadata line
        metadata_parts = []
        if record.get('author'):
            metadata_parts.append(f"Author: {record['author']}")
        if record.get('camera_make'):
            metadata_parts.append(f"Camera: {record['camera_make']} {record.get('camera_model', '')}")
        if record.get('size'):
            size_str = self._format_size(record['size'])
            metadata_parts.append(f"Size: {size_str}")

        if metadata_parts:
            metadata_label = ctk.CTkLabel(
                card,
                text=" • ".join(metadata_parts[:3]),
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            )
            metadata_label.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        # Path
        path_label = ctk.CTkLabel(
            card,
            text=record['path'],
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        path_label.grid(row=2, column=1, sticky="w", padx=10, pady=(2, 10))

        # Open button
        open_button = ctk.CTkButton(
            card,
            text="Open",
            command=lambda: self._open_file(record['path']),
            width=80,
            height=32
        )
        open_button.grid(row=0, column=2, rowspan=3, padx=20, pady=10)

    def _open_file(self, path: str):
        """Open file in default application"""
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                os.system(f'open "{path}"')
            else:
                os.system(f'xdg-open "{path}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def _show_statistics(self):
        """Show statistics dialog"""
        stats = self.db.get_statistics()

        stats_window = ctk.CTkToplevel(self)
        stats_window.title("MetaFinder Statistics")
        stats_window.geometry("600x500")

        # Title
        title = ctk.CTkLabel(
            stats_window,
            text="📊 Database Statistics",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)

        # Stats frame
        stats_frame = ctk.CTkFrame(stats_window)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Total files
        ctk.CTkLabel(
            stats_frame,
            text=f"Total Files: {stats['total_files']}",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)

        # Total size
        total_size = self._format_size(stats['total_size_bytes'])
        ctk.CTkLabel(
            stats_frame,
            text=f"Total Size: {total_size}",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)

        # By type
        if stats['by_type']:
            ctk.CTkLabel(
                stats_frame,
                text="\nFiles by Type:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(pady=(20, 10))

            for file_type, count in stats['by_type'].items():
                ctk.CTkLabel(
                    stats_frame,
                    text=f"  {file_type}: {count}",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=2)

        # Top extensions
        if stats['top_extensions']:
            ctk.CTkLabel(
                stats_frame,
                text="\nTop Extensions:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(pady=(20, 10))

            for ext, count in list(stats['top_extensions'].items())[:10]:
                ctk.CTkLabel(
                    stats_frame,
                    text=f"  {ext}: {count}",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=2)

    def _update_status(self, message: str):
        """Update status bar"""
        self.status_label.configure(text=message)

    def _format_size(self, bytes_size: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} PB"


def main():
    """Main entry point"""
    app = MetaFinderGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
