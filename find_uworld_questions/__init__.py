"""
Find UWorld Questions Add-on for Anki
Extracts UWorld question IDs from selected cards/notes in the Browser
"""

import re
import os
from typing import Set, List
from aqt import mw, gui_hooks
from aqt.qt import (
    QAction, QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, 
    QTabWidget, QWidget, QLabel, QApplication, QMessageBox, QCheckBox, 
    QFont, QPixmap, QIcon, QPalette, QColor, Qt
)
from anki.notes import Note

# Regex patterns for UWorld tag extraction
RE_STEP1 = re.compile(r"#AK_Step1_v\d+::#UWorld::Step::(\d+)\b")
RE_STEP2 = re.compile(r"#AK_Step2_v\d+::#UWorld::Step::(\d+)\b")
RE_STEP3 = re.compile(r"#AK_Step3_v\d+::#UWorld::(?!COMLEX::)(\d+)\b")
RE_COMLEX1 = re.compile(r"#AK_Step1_v\d+::#UWorld::COMLEX::(\d+)\b")
RE_COMLEX2 = re.compile(r"#AK_Step2_v\d+::#UWorld::COMLEX::(\d+)\b")

class UWorldQuestionFinder:
    """Main class for extracting UWorld question IDs from notes"""
    
    def __init__(self):
        self.ids_step1: Set[int] = set()
        self.ids_step2: Set[int] = set()
        self.ids_step3: Set[int] = set()
        self.ids_comlex1: Set[int] = set()
        self.ids_comlex2: Set[int] = set()
    
    def extract_ids_from_notes(self, notes: List[Note]) -> None:
        """Extract UWorld IDs from a list of notes"""
        self.ids_step1.clear()
        self.ids_step2.clear()
        self.ids_step3.clear()
        self.ids_comlex1.clear()
        self.ids_comlex2.clear()
        
        for note in notes:
            for tag in note.tags:
                self._extract_ids_from_tag(tag)
    
    def _extract_ids_from_tag(self, tag: str) -> None:
        """Extract IDs from a single tag"""
        # Step 1
        match = RE_STEP1.search(tag)
        if match:
            self.ids_step1.add(int(match.group(1)))
            return
        
        # Step 2
        match = RE_STEP2.search(tag)
        if match:
            self.ids_step2.add(int(match.group(1)))
            return
        
        # Step 3
        match = RE_STEP3.search(tag)
        if match:
            self.ids_step3.add(int(match.group(1)))
            return
        
        # COMLEX 1
        match = RE_COMLEX1.search(tag)
        if match:
            self.ids_comlex1.add(int(match.group(1)))
            return
        
        # COMLEX 2
        match = RE_COMLEX2.search(tag)
        if match:
            self.ids_comlex2.add(int(match.group(1)))
            return
    
    def get_ids_for_category(self, category: str) -> List[int]:
        """Get sorted list of IDs for a specific category"""
        if category == "Step 1":
            return sorted(list(self.ids_step1))
        elif category == "Step 2":
            return sorted(list(self.ids_step2))
        elif category == "Step 3":
            return sorted(list(self.ids_step3))
        elif category == "COMLEX 1":
            return sorted(list(self.ids_comlex1))
        elif category == "COMLEX 2":
            return sorted(list(self.ids_comlex2))
        return []


class UWorldDialog(QDialog):
    """Dialog for displaying and managing UWorld question IDs"""
    
    def __init__(self, finder: UWorldQuestionFinder, parent=None):
        super().__init__(parent)
        self.finder = finder
        self.current_category = "Step 1"
        self.setup_ui()
        self.update_display()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Find UWorld Questions")
        self.setMinimumSize(700, 500)
        
        # Apply UWorld color scheme
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QTabWidget {
                border: none;
                outline: none;
            }
            QTabWidget::pane {
                border: none;
                background-color: transparent;
                outline: none;
            }
            QTabWidget::tab-bar {
                alignment: left;
                border: none;
                outline: none;
            }
            QTabBar {
                alignment: left;
                border: none;
                outline: none;
                background: transparent;
            }
            QTabBar::tab-bar {
                border: none;
                outline: none;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                padding: 10px 20px;
                margin-right: 3px;
                border-radius: 8px;
                border: none;
                outline: none;
            }
            QTabBar::tab:selected {
                background-color: #007bff;
                color: white;
                border: none;
                outline: none;
            }
            QTabBar::tab:hover {
                background-color: #0056b3;
                color: white;
                border: none;
                outline: none;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QTextEdit {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                padding: 12px;
                color: #007bff;
                font-weight: bold;
            }
            QCheckBox {
                color: #495057;
            }
            QLabel {
                color: #495057;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with UWorld logo
        header_layout = QHBoxLayout()
        
        # Add UWorld logo if available
        addon_dir = os.path.dirname(__file__)
        logo_path = os.path.join(addon_dir, "UWorld.jpg")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Scale logo to appropriate size
                scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
                header_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Find UWorld Questions")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #007bff; margin-left: 2px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Tab widget for categories
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setDocumentMode(True)  # Remove the frame around tabs
        self.tab_widget.setUsesScrollButtons(False)  # Prevent scroll buttons
        categories = ["Step 1", "Step 2", "Step 3", "COMLEX 1", "COMLEX 2"]
        
        for category in categories:
            tab = QWidget()
            self.tab_widget.addTab(tab, category)
        
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Create a container widget to control tab alignment
        tab_container = QWidget()
        tab_layout = QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        tab_layout.addWidget(self.tab_widget)
        tab_layout.addStretch()  # Push tabs to the left
        
        layout.addWidget(tab_container)
        
        # Count label
        self.count_label = QLabel()
        count_font = QFont()
        count_font.setBold(True)
        self.count_label.setFont(count_font)
        self.count_label.setStyleSheet("color: #007bff; font-size: 14px;")
        layout.addWidget(self.count_label)
        
        # Text area for displaying IDs
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        font = QFont("Consolas", 11)
        if not font.exactMatch():
            font = QFont("Courier New", 11)
        self.text_area.setFont(font)
        self.text_area.setMinimumHeight(200)
        layout.addWidget(self.text_area)
        
        # Options
        options_layout = QHBoxLayout()
        self.spaces_checkbox = QCheckBox("Copy with spaces after commas")
        self.spaces_checkbox.setChecked(True)
        options_layout.addWidget(self.spaces_checkbox)
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button)
        
        button_layout.addStretch()
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # Credits
        credits_layout = QHBoxLayout()
        credits_layout.addStretch()
        credits_label = QLabel('Made by <a href="https://ashklab.com" style="color: #007bff; text-decoration: none;">Yusuf Ashktorab</a>')
        credits_label.setOpenExternalLinks(True)
        credits_label.setStyleSheet("color: #6c757d; font-size: 10px;")
        credits_layout.addWidget(credits_label)
        layout.addLayout(credits_layout)
    
    def on_tab_changed(self, index: int):
        """Handle tab change"""
        categories = ["Step 1", "Step 2", "Step 3", "COMLEX 1", "COMLEX 2"]
        self.current_category = categories[index]
        self.update_display()
    
    def update_display(self):
        """Update the display with current category data"""
        ids = self.finder.get_ids_for_category(self.current_category)
        count = len(ids)
        
        # Update count label
        self.count_label.setText(f"{self.current_category}: {count} Questions")
        
        # Update text area
        if ids:
            id_text = ", ".join(str(id_num) for id_num in ids)
            self.text_area.setPlainText(id_text)
        else:
            self.text_area.setPlainText("")
    
    def get_current_ids_text(self, with_spaces: bool = True) -> str:
        """Get current IDs as formatted text"""
        ids = self.finder.get_ids_for_category(self.current_category)
        if not ids:
            return ""
        
        separator = ", " if with_spaces else ","
        return separator.join(str(id_num) for id_num in ids)
    
    def copy_to_clipboard(self):
        """Copy current IDs to clipboard"""
        text = self.get_current_ids_text(self.spaces_checkbox.isChecked())
        QApplication.clipboard().setText(text)
        
        if text:
            QMessageBox.information(self, "Copied", f"Copied {len(text.split(','))} Questions to clipboard")
        else:
            QMessageBox.information(self, "Copied", "No Questions to copy")
    


def get_selected_notes() -> List[Note]:
    """Get selected notes from the browser"""
    browser = mw.app.activeWindow()
    if not hasattr(browser, 'selectedNotes'):
        return []
    
    # Try to get selected notes first
    note_ids = browser.selectedNotes()
    if note_ids:
        return [mw.col.getNote(nid) for nid in note_ids]
    
    # Fallback to selected cards and convert to notes
    card_ids = browser.selectedCards()
    if card_ids:
        note_ids = set()
        for cid in card_ids:
            card = mw.col.getCard(cid)
            note_ids.add(card.nid)
        return [mw.col.getNote(nid) for nid in note_ids]
    
    return []


def show_uworld_dialog():
    """Show the UWorld question finder dialog"""
    notes = get_selected_notes()
    
    if not notes:
        QMessageBox.warning(
            mw.app.activeWindow(), 
            "No Selection", 
            "Select at least one note or card in the Browser."
        )
        return
    
    finder = UWorldQuestionFinder()
    finder.extract_ids_from_notes(notes)
    
    dialog = UWorldDialog(finder, mw.app.activeWindow())
    dialog.exec()


def add_browser_context_menu(browser, menu):
    """Add context menu item to browser"""
    action = QAction("Find UWorld Questions...", menu)
    action.triggered.connect(show_uworld_dialog)
    menu.addAction(action)


# Initialize the add-on
def init_addon():
    """Initialize the add-on"""
    gui_hooks.browser_will_show_context_menu.append(add_browser_context_menu)


# Start the add-on when Anki loads
init_addon()
