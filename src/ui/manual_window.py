"""
Manual Mode Window - Load XML from manual input
"""
from typing import Optional
from PySide6.QtWidgets import QPushButton, QTextEdit, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from .base_xml_window import BaseXMLWindow


class ManualWindow(BaseXMLWindow):
    """Manual mode window for loading XML from manual text input."""

    def __init__(self) -> None:
        super().__init__(
            window_title="🌐 SocialNet XML Parser - Manual Mode",
            mode_name="Manual mode"
        )

    def _setup_input_section(self, parent_layout: QVBoxLayout) -> None:
        """Set up the text editor input section."""
        # Text area
        text_widget = QWidget()
        text_widget.setObjectName("textPanel")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(20, 20, 20, 20)
        text_layout.setSpacing(10)

        text_title_layout = QHBoxLayout()
        text_title_layout.setContentsMargins(5, 5, 5, 5)
        text_title_layout.setSpacing(40)

        text_title = QLabel("Enter XML Data")
        text_title.setStyleSheet("""
            QLabel {
                color: rgba(100, 230, 255, 255);
                font-size: 22px;
                font-weight: bold;
            }
        """)

        upload_btn = QPushButton("⬆ Upload")
        upload_btn.setObjectName("uploadBtn")
        upload_btn.setMinimumHeight(40)
        upload_btn.setMaximumWidth(150)
        upload_btn.clicked.connect(self.upload_and_parse)

        text_title_layout.addWidget(text_title)
        text_title_layout.addWidget(upload_btn)

        text_layout.addLayout(text_title_layout)

        self.text_data = QTextEdit()
        self.text_data.setPlaceholderText("Enter your Social Network XML Data here")
        self.text_data.setObjectName("textInput")
        self.text_data.setMinimumHeight(40)

        text_layout.addWidget(self.text_data, 1)
        parent_layout.addWidget(text_widget)

    def _get_panel_selector(self) -> str:
        """Return the panel selector for stylesheet."""
        return "#textPanel, #resultPanel, #opsPanel"

    def _get_initialization_message(self) -> str:
        """Return the initialization message."""
        return "Ready to load XML text."

    def browse_file(self) -> None:
        """Handle file browsing - not used in manual mode."""
        pass

    def upload_and_parse(self) -> None:
        """Handle XML text upload and parsing."""
        if not hasattr(self, 'text_data') or not self.text_data:
            self.log_message("ERROR: Text input not available.")
            return

        xml_text = self.text_data.toPlainText()
        if not xml_text.strip():
            self.log_message("ERROR: No XML text entered.")
            QMessageBox.warning(self, "No Data", "Please enter XML data first.")
            return

        self.log_message("User initiated upload and parse for manual input.")

        if self.xml_controller:
            success, message, user_count = self.xml_controller.parse_xml_string(xml_text)

            if success:
                self.current_file_path = ""  # No file path for manual input
                self.user_record_count = user_count

                xml_data = self.xml_controller.get_xml_data()
                if self.data_controller:
                    self.data_controller.set_xml_data(xml_data)
                if self.graph_controller:
                    self.graph_controller.set_xml_data(xml_data)

                self.log_message("Loading XML from text input...")
                self.log_message(message)
                self.log_message("✓ Parsing completed. Data ready for operations.")

                QMessageBox.information(
                    self,
                    "Success",
                    f"XML parsed successfully!\n\nFound {user_count} user records.\nData is ready for operations."
                )
            else:
                self.log_message(f"ERROR: {message}")
                QMessageBox.critical(self, "Error", f"Failed to parse XML:\n{message}")
