"""
Code Viewer Window - UI component for displaying code in a read-only window.
"""

from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont
import re


class CodeViewerWindow(QWidget):
    """Window for viewing code in read-only mode."""
    
    def __init__(self, code_text: str, main_window_size: QSize, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.code_text: str = code_text
        self.main_window_size: QSize = main_window_size
        self.code_editor: Optional[QTextEdit] = None
        self.setup_ui()
    
    def setup_ui(self) -> None:
        self.setWindowTitle("Code (Read-only) Window")
        # Set the same size as the main window
        self.resize(self.main_window_size)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #d4d4d4; border-bottom: 1px solid #a0a0a0;")
        title_bar.setFixedHeight(30)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        title_label = QLabel("Code (Read-only) Window")
        title_label.setStyleSheet("color: #333; font-size: 12px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #666;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        # Code editor
        self.code_editor = QTextEdit()
        self.code_editor.setReadOnly(True)
        self.code_editor.setPlainText(self.code_text)
        
        # Styling for code editor
        font = QFont("Consolas", 10)
        font.setFixedPitch(True)
        self.code_editor.setFont(font)
        
        self.code_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                padding: 10px;
                selection-background-color: #264f78;
            }
        """)
        
        # Status bar
        status_bar = QWidget()
        status_bar.setStyleSheet("background-color: #007acc; border-top: 1px solid #005a9e;")
        status_bar.setFixedHeight(25)
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 10, 0)
        
        status_label = QLabel("Read-only Mode")
        status_label.setStyleSheet("color: white; font-size: 11px;")
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        
        # Add line count
        line_count = len(self.code_text.split('\n'))
        line_label = QLabel(f"Lines: {line_count}")
        line_label.setStyleSheet("color: white; font-size: 11px;")
        status_layout.addWidget(line_label)
        
        # Add widgets to main layout
        layout.addWidget(title_bar)
        layout.addWidget(self.code_editor)
        layout.addWidget(status_bar)
        
        # Apply syntax highlighting (basic)
        self.apply_syntax_highlighting()
    
    def apply_syntax_highlighting(self) -> None:
        """Apply syntax highlighting to the code."""
        # Get the text
        text = self.code_editor.toPlainText()
        
        # Check if content is XML
        is_xml = text.strip().startswith('<?xml') or text.strip().startswith('<')
        
        if is_xml:
            # For XML, display as plain text to avoid breaking the structure
            self.code_editor.setPlainText(text)
        else:
            # JavaScript/React syntax highlighting
            highlighted_text = text
            
            # Keywords
            keywords = ['import', 'from', 'const', 'if', 'return', 'new', 'export', 'default']
            for keyword in keywords:
                highlighted_text = highlighted_text.replace(
                    f' {keyword} ', 
                    f' <span style="color: #569cd6;">{keyword}</span> '
                )
                highlighted_text = highlighted_text.replace(
                    f'{keyword} ', 
                    f'<span style="color: #569cd6;">{keyword}</span> '
                )
            
            # Strings
            highlighted_text = re.sub(
                r'"([^"]*)"',
                r'<span style="color: #ce9178;">"\1"</span>',
                highlighted_text
            )
            highlighted_text = re.sub(
                r"'([^']*)'",
                r"<span style='color: #ce9178;'>'\1'</span>",
                highlighted_text
            )
            
            # Comments
            highlighted_text = re.sub(
                r'(//.*?)$',
                r'<span style="color: #6a9955;">\1</span>',
                highlighted_text,
                flags=re.MULTILINE
            )
            
            # Set HTML
            self.code_editor.setHtml(
                f'<pre style="font-family: Consolas, monospace; font-size: 10pt;">{highlighted_text}</pre>'
            )

