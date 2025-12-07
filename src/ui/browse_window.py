"""
Browse Mode Window - Load XML from file browser
"""
from typing import Optional
from PySide6.QtWidgets import QPushButton, QLineEdit, QFileDialog, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

from .base_xml_window import BaseXMLWindow


class BrowseWindow(BaseXMLWindow):
    """Browse mode window for loading XML from files."""

    def __init__(self) -> None:
        super().__init__(
            window_title="🌐 SocialNet XML Parser - Browse Mode",
            mode_name="Browse mode"
        )

    def _setup_input_section(self, parent_layout: QVBoxLayout) -> None:
        """Set up the file browser input section."""
        # File selection area
        file_widget = QWidget()
        file_widget.setObjectName("filePanel")
        file_layout = QVBoxLayout(file_widget)
        file_layout.setContentsMargins(20, 20, 20, 20)
        file_layout.setSpacing(15)

        file_title = QLabel("Load XML Data")
        file_title.setStyleSheet("""
            QLabel {
                color: rgba(100, 230, 255, 255);
                font-size: 22px;
                font-weight: bold;
            }
        """)
        file_layout.addWidget(file_title)

        file_input_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("/path/to/your/file.xml")
        self.file_path_edit.setObjectName("fileInput")
        self.file_path_edit.setMinimumHeight(40)

        browse_btn = QPushButton("📁 Browse")
        browse_btn.setObjectName("browseFileBtn")
        browse_btn.setMinimumHeight(40)
        browse_btn.setMinimumWidth(120)
        browse_btn.clicked.connect(self.browse_file)

        upload_btn = QPushButton("⬆ Upload & Parse")
        upload_btn.setObjectName("uploadBtn")
        upload_btn.setMinimumHeight(40)
        upload_btn.setMinimumWidth(180)
        upload_btn.clicked.connect(self.upload_and_parse)

        file_input_layout.addWidget(self.file_path_edit)
        file_input_layout.addWidget(browse_btn)
        file_input_layout.addWidget(upload_btn)

        file_layout.addLayout(file_input_layout)
        parent_layout.addWidget(file_widget)

    def _get_panel_selector(self) -> str:
        """Return the panel selector for stylesheet."""
        return "#filePanel, #resultPanel, #opsPanel"

    def _get_initialization_message(self) -> str:
        """Return the initialization message."""
        return "Ready to load XML file."

    def browse_file(self) -> None:
        """Handle file browsing."""
        self.log_message("User clicked Browse button.")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select XML File",
            "",
            "XML Files (*.xml);;All Files (*)"
        )
        if file_path:
            if self.file_path_edit:
                self.file_path_edit.setText(file_path)
            self.current_file_path = file_path
            self.log_message(f"User selected file: {file_path}")
        else:
            self.log_message("User cancelled file selection.")

    def upload_and_parse(self) -> None:
        """Handle file upload and parsing."""
        if not self.file_path_edit:
            self.log_message("ERROR: File path input not available.")
            return

        file_path = self.file_path_edit.text()
        if not file_path:
            self.log_message("ERROR: No file selected.")
            QMessageBox.warning(self, "No File", "Please select an XML file first.")
            return

        self.log_message(f"User initiated upload and parse for: {file_path}")

        if self.xml_controller:
            success, message, user_count = self.xml_controller.parse_xml_file(file_path)

            if success:
                self.current_file_path = file_path
                self.user_record_count = user_count

                xml_data = self.xml_controller.get_xml_data()
                if self.data_controller:
                    self.data_controller.set_xml_data(xml_data)
                if self.graph_controller:
                    self.graph_controller.set_xml_data(xml_data)

                self.log_message(f"Loading file: {file_path}...")
                self.log_message(message)
                self.log_message("✓ Parsing completed. Data ready for operations.")

                QMessageBox.information(
                    self,
                    "Success",
                    f"File loaded successfully!\n\nFound {user_count} user records.\nData is ready for operations."
                )
            else:
                self.log_message(f"ERROR: {message}")
                QMessageBox.critical(self, "Error", f"Failed to load file:\n{message}")
