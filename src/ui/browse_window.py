"""
Browse Mode Window - Load XML from file browser
"""
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QTextEdit, QLineEdit, QFileDialog,
                              QMessageBox, QLabel)
from PySide6.QtCore import Qt, Signal


class BrowseWindow(QMainWindow):
    """Browse mode window for loading XML from files."""

    back_clicked = Signal()

    def __init__(self):
        super().__init__()

        # Import controllers
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))

        try:
            from controllers.xml_controller import XMLController
            from controllers.data_controller import DataController
            from controllers.graph_controller import GraphController
            self.xml_controller = XMLController()
            self.data_controller = DataController()
            self.graph_controller = GraphController()
        except ImportError:
            self.xml_controller = None
            self.data_controller = None
            self.graph_controller = None

        self.current_file_path = ""
        self.user_record_count = 0

        self.setup_ui()
        self.apply_stylesheet()
        self.log_message("Browse mode initialized.")
        self.log_message("Ready to load XML file.")

    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("🌐 SocialNet XML Parser - Browse Mode")
        self.setMinimumSize(1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Top bar with back button
        top_bar = QHBoxLayout()

        back_btn = QPushButton("← Back to Home")
        back_btn.setObjectName("backBtn")
        back_btn.setMinimumHeight(40)
        back_btn.setMinimumWidth(150)
        back_btn.clicked.connect(self.back_clicked.emit)
        top_bar.addWidget(back_btn)
        top_bar.addStretch()

        main_layout.addLayout(top_bar)

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
                font-size: 18px;
                font-weight: bold;
            }
        """)
        file_layout.addWidget(file_title)

        file_label = QLabel("Select Social Network User Data File (XML)")
        file_label.setStyleSheet("color: rgba(200, 210, 220, 255); font-size: 13px;")
        file_layout.addWidget(file_label)

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
        main_layout.addWidget(file_widget)

        # Content area - Log and Operations
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)

        # Left side - Operation Log
        log_widget = QWidget()
        log_widget.setObjectName("logPanel")
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(20, 20, 20, 20)
        log_layout.setSpacing(15)

        log_title = QLabel("Operation Log")
        log_title.setStyleSheet("""
            QLabel {
                color: rgba(100, 230, 255, 255);
                font-size: 18px;
                font-weight: bold;
            }
        """)
        log_layout.addWidget(log_title)

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setObjectName("logText")
        log_layout.addWidget(self.log_text_edit)

        # Right side - Operations
        ops_widget = QWidget()
        ops_widget.setObjectName("opsPanel")
        ops_layout = QVBoxLayout(ops_widget)
        ops_layout.setContentsMargins(20, 20, 20, 20)
        ops_layout.setSpacing(15)

        ops_title = QLabel("Operations")
        ops_title.setStyleSheet("""
            QLabel {
                color: rgba(100, 230, 255, 255);
                font-size: 18px;
                font-weight: bold;
            }
        """)
        ops_layout.addWidget(ops_title)

        parse_label = QLabel("Parsing & Validation")
        parse_label.setStyleSheet("color: rgba(180, 200, 220, 255); font-weight: bold; margin-top: 10px;")
        ops_layout.addWidget(parse_label)

        parsing_ops = [
            ("📋 Validate XML Structure", self.validate_xml),
            ("⚙ Parse User Data", self.parse_user_data),
            ("⚠ Check for Errors", self.check_for_errors),
            ("✨ Format XML", self.format_xml),
            ("📝 View Code", self.view_code),
        ]

        for text, handler in parsing_ops:
            btn = QPushButton(text)
            btn.setObjectName("operationBtn")
            btn.setMinimumHeight(42)
            btn.clicked.connect(handler)
            ops_layout.addWidget(btn)

        viz_label = QLabel("Visualization")
        viz_label.setStyleSheet("color: rgba(180, 200, 220, 255); font-weight: bold; margin-top: 15px;")
        ops_layout.addWidget(viz_label)

        viz_ops = [
            ("🔗 Visualize Network Graph", self.visualize_network),
            ("📊 Show User Statistics", self.show_user_stats),
            ("📄 Export to JSON", self.export_to_json),
        ]

        for text, handler in viz_ops:
            btn = QPushButton(text)
            btn.setObjectName("operationBtn")
            btn.setMinimumHeight(42)
            btn.clicked.connect(handler)
            ops_layout.addWidget(btn)

        ops_layout.addStretch()

        content_layout.addWidget(log_widget, 2)
        content_layout.addWidget(ops_widget, 1)

        main_layout.addLayout(content_layout)

    def apply_stylesheet(self):
        """Apply modern stylesheet matching landing page."""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 rgba(10, 15, 30, 255),
                                           stop:1 rgba(15, 25, 40, 255));
            }
            
            #filePanel, #logPanel, #opsPanel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 rgba(20, 35, 55, 200),
                                           stop:1 rgba(15, 25, 45, 200));
                border: 2px solid rgba(100, 150, 200, 100);
                border-radius: 15px;
            }
            
            #fileInput {
                background-color: rgba(30, 45, 65, 180);
                border: 1px solid rgba(80, 120, 160, 120);
                border-radius: 8px;
                color: rgba(220, 230, 240, 255);
                padding: 10px;
                font-size: 13px;
            }
            
            #logText {
                background-color: rgba(15, 20, 35, 180);
                border: 1px solid rgba(80, 120, 160, 120);
                border-radius: 8px;
                color: rgba(220, 230, 240, 255);
                padding: 12px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            
            #backBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 rgba(60, 80, 100, 200),
                                           stop:1 rgba(80, 100, 120, 200));
                border: 2px solid rgba(100, 150, 200, 150);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
            }
            
            #backBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 rgba(80, 100, 120, 230),
                                           stop:1 rgba(100, 120, 140, 230));
            }
            
            #browseFileBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 rgba(40, 120, 200, 200),
                                           stop:1 rgba(60, 140, 220, 200));
                border: 2px solid rgba(80, 160, 240, 200);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            
            #browseFileBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 rgba(60, 140, 220, 230),
                                           stop:1 rgba(80, 160, 240, 230));
            }
            
            #uploadBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 rgba(50, 150, 255, 200),
                                           stop:1 rgba(80, 180, 255, 200));
                border: 2px solid rgba(100, 200, 255, 255);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            
            #uploadBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 rgba(70, 170, 255, 230),
                                           stop:1 rgba(100, 200, 255, 230));
            }
            
            #operationBtn {
                background: rgba(40, 70, 110, 180);
                border: 1px solid rgba(80, 120, 180, 150);
                border-radius: 8px;
                color: rgba(200, 220, 240, 255);
                font-size: 13px;
                text-align: left;
                padding-left: 15px;
            }
            
            #operationBtn:hover {
                background: rgba(60, 90, 130, 200);
                border: 1px solid rgba(100, 150, 200, 180);
                color: white;
            }
            
            #operationBtn:pressed {
                background: rgba(30, 50, 80, 180);
            }
        """)

    def log_message(self, message):
        """Log a message to the operation log."""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log_text_edit.append(f"{timestamp} {message}")

    def browse_file(self):
        """Handle file browsing."""
        self.log_message("User clicked Browse button.")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select XML File",
            "",
            "XML Files (*.xml);;All Files (*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
            self.current_file_path = file_path
            self.log_message(f"User selected file: {file_path}")
        else:
            self.log_message("User cancelled file selection.")

    def upload_and_parse(self):
        """Handle file upload and parsing."""
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

    # Operation methods - Connect to controllers
    def validate_xml(self):
        self.log_message("Validating XML structure...")
        # Connect to controller

    def parse_user_data(self):
        self.log_message("Parsing user data...")
        # Connect to controller

    def check_for_errors(self):
        self.log_message("Checking for errors...")
        # Connect to controller

    def format_xml(self):
        self.log_message("Formatting XML...")
        # Connect to controller

    def view_code(self):
        self.log_message("Opening code viewer...")
        # Connect to controller

    def visualize_network(self):
        self.log_message("Visualizing network...")
        # Connect to controller

    def show_user_stats(self):
        self.log_message("Calculating statistics...")
        # Connect to controller

    def export_to_json(self):
        self.log_message("Exporting to JSON...")
        # Connect to controller