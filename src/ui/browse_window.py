"""
Browse Mode Window - Load XML from file browser
"""
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QTextEdit, QLineEdit, QFileDialog,
                           QMessageBox, QLabel)
from PySide6.QtCore import Qt, Signal

# Controller imports
from ..controllers import XMLController, DataController, GraphController

# UI window imports
from .code_viewer_window import CodeViewerWindow
from .graph_visualization_window import GraphVisualizationWindow



class BrowseWindow(QMainWindow):
    """Browse mode window for loading XML from files."""

    """Base class for XML operation windows with shared functionality."""

    back_clicked = Signal()

    def __init__(self, window_title="🌐 SocialNet XML Parser", mode_name="XML Mode"):
        super().__init__()

        # Initialize controllers
        self.xml_controller = XMLController()
        self.data_controller = DataController()
        self.graph_controller = GraphController()

        self.current_file_path = ""
        self.user_record_count = 0
        self.window_title = window_title
        self.mode_name = mode_name

        self.setup_ui()
        self.apply_stylesheet()
        self.log_message(f"{mode_name} initialized.")
        self.log_message("Ready to load XML file.")

    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle(self.window_title)
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

        # container for the grid layout
        sub_layout = QHBoxLayout()
        sub_layout.setSpacing(15)

        main_layout.addLayout(sub_layout)

        # Left side - file explorer + Operation Log
        left_widget = QWidget()
        left_widget.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(15)

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
        left_layout.addWidget(file_widget)

        # Result (Read-Only) area - to be refactored
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
        left_layout.addWidget(log_widget)

        sub_layout.addWidget(left_widget)

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

        parsing_ops = [
            ("📋 Validate XML Structure", self.validate_xml),
            ("⚙ Correct Errors", self.parse_user_data),
            ("✨ Format XML", self.format_xml),
            ("Compress File", self.check_for_errors),
            ("Decompress File", self.view_code),
            ("Minify XML", self.view_code),
            ("📄 Export to JSON", self.export_to_json),
            ("🔗 Visualize Network Graph", self.visualize_network),
            ("📊 Show Users Statistics", self.show_user_stats),
            ("🔍 Search for Topic/Posts", self.show_user_stats)
        ]

        for text, handler in parsing_ops:
            btn = QPushButton(text)
            btn.setObjectName("operationBtn")
            btn.setMinimumHeight(42)
            btn.clicked.connect(handler)
            ops_layout.addWidget(btn)

        ops_layout.addStretch()

        sub_layout.addWidget(ops_widget)

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
        """Validate XML structure."""
        if not self.current_file_path:
            self.log_message("ERROR: No file loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No File", "Please upload and parse an XML file first.")
            return

        self.log_message("Validating XML structure...")

        if not self.xml_controller:
            self.log_message("ERROR: XML controller not available.")
            QMessageBox.critical(self, "Error", "XML controller not available.")
            return

        success, details, error = self.xml_controller.validate_xml_structure(self.current_file_path)

        if success:
            self.log_message("✓ XML validation successful!")
            for detail in details:
                self.log_message(f"  {detail}")
            QMessageBox.information(
                self,
                "Validation Success",
                "XML structure is valid!\n\n" + "\n".join(details)
            )
        else:
            self.log_message(f"✗ Validation failed: {error}")
            QMessageBox.critical(self, "Validation Failed", f"XML validation failed:\n{error}")

    def parse_user_data(self):
        """Parse user data and show statistics."""
        if not self.data_controller or not self.data_controller.xml_data:
            self.log_message("ERROR: No data loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No Data", "Please upload and parse an XML file first.")
            return

        self.log_message("Parsing user data...")

        success, stats, error = self.data_controller.parse_user_data()

        if success:
            self.log_message("✓ User data parsed successfully!")
            self.log_message(f"  Total users: {stats.get('total_users', 0)}")
            self.log_message(f"  Total followers: {stats.get('total_followers', 0)}")
            self.log_message(f"  Total following: {stats.get('total_following', 0)}")
            self.log_message(f"  Total posts: {stats.get('total_posts', 0)}")

            if 'sample_user' in stats and stats['sample_user']:
                sample = stats['sample_user']
                self.log_message(
                    f"  Sample user: ID={sample.get('id', 'N/A')}, Username={sample.get('username', 'N/A')}")

            stats_text = (
                f"Total Users: {stats.get('total_users', 0)}\n"
                f"Total Followers: {stats.get('total_followers', 0)}\n"
                f"Total Following: {stats.get('total_following', 0)}\n"
                f"Total Posts: {stats.get('total_posts', 0)}"
            )
            QMessageBox.information(self, "Parse Results", stats_text)
        else:
            self.log_message(f"✗ Parse failed: {error}")
            QMessageBox.critical(self, "Parse Failed", f"Failed to parse user data:\n{error}")

    def check_for_errors(self):
        """Check for data integrity issues."""
        if not self.data_controller or not self.data_controller.xml_data:
            self.log_message("ERROR: No data loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No Data", "Please upload and parse an XML file first.")
            return

        self.log_message("Checking for errors...")

        success, errors, warnings, error_msg = self.data_controller.check_for_errors()

        if not success:
            self.log_message(f"✗ Error check failed: {error_msg}")
            QMessageBox.critical(self, "Error Check Failed", f"Failed to check for errors:\n{error_msg}")
            return

        self.log_message(f"✓ Error check completed. Found {len(errors)} errors and {len(warnings)} warnings.")

        if errors:
            self.log_message("Errors found:")
            for err in errors:
                self.log_message(f"  ✗ {err}")

        if warnings:
            self.log_message("Warnings found:")
            for warn in warnings:
                self.log_message(f"  ⚠ {warn}")

        if not errors and not warnings:
            self.log_message("  ✓ No errors or warnings found. Data is clean!")
            QMessageBox.information(self, "No Issues", "No errors or warnings found. Data is clean!")
        else:
            result_text = ""
            if errors:
                result_text += f"Errors ({len(errors)}):\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    result_text += f"\n... and {len(errors) - 10} more errors"
                result_text += "\n\n"
            if warnings:
                result_text += f"Warnings ({len(warnings)}):\n" + "\n".join(warnings[:10])
                if len(warnings) > 10:
                    result_text += f"\n... and {len(warnings) - 10} more warnings"

            QMessageBox.warning(self, "Issues Found", result_text)

    def format_xml(self):
        """Format/prettify XML file."""
        if not self.current_file_path:
            self.log_message("ERROR: No file loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No File", "Please upload and parse an XML file first.")
            return

        self.log_message("Formatting XML...")

        if not self.xml_controller:
            self.log_message("ERROR: XML controller not available.")
            QMessageBox.critical(self, "Error", "XML controller not available.")
            return

        success, message = self.xml_controller.format_xml_file(self.current_file_path)

        if success:
            self.log_message(f"✓ {message}")
            QMessageBox.information(self, "Format Success", message)
        else:
            self.log_message(f"✗ Format failed: {message}")
            QMessageBox.critical(self, "Format Failed", f"Failed to format XML:\n{message}")

    def view_code(self):
        """View XML file content in code viewer."""
        if not self.current_file_path:
            self.log_message("ERROR: No file loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No File", "Please upload and parse an XML file first.")
            return

        self.log_message("Opening code viewer...")

        if not self.xml_controller:
            self.log_message("ERROR: XML controller not available.")
            QMessageBox.critical(self, "Error", "XML controller not available.")
            return

        success, content, error = self.xml_controller.read_xml_file_content(self.current_file_path)

        if success:
            try:
                code_window = CodeViewerWindow(content, self.size(), self)
                code_window.show()
                self.log_message("✓ Code viewer opened successfully.")
            except Exception as e:
                self.log_message(f"ERROR: Failed to open code viewer: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to open code viewer:\n{str(e)}")
        else:
            self.log_message(f"✗ Failed to read file: {error}")
            QMessageBox.critical(self, "Read Failed", f"Failed to read file:\n{error}")

    def visualize_network(self):
        """Visualize network graph."""
        if not self.graph_controller or not self.graph_controller.xml_data:
            self.log_message("ERROR: No data loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No Data", "Please upload and parse an XML file first.")
            return

        self.log_message("Building network graph...")

        success, nodes, edges, error = self.graph_controller.build_graph()

        if success:
            self.log_message(f"✓ Graph built successfully! Nodes: {len(nodes)}, Edges: {len(edges)}")
            try:
                graph_window = GraphVisualizationWindow(nodes, edges, self.size(), self)
                graph_window.show()
                self.log_message("✓ Graph visualization window opened.")
            except Exception as e:
                self.log_message(f"ERROR: Failed to open graph window: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to open graph visualization:\n{str(e)}")
        else:
            self.log_message(f"✗ Graph build failed: {error}")
            QMessageBox.critical(self, "Graph Build Failed", f"Failed to build graph:\n{error}")

    def show_user_stats(self):
        """Show user statistics."""
        if not self.data_controller or not self.data_controller.xml_data:
            self.log_message("ERROR: No data loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No Data", "Please upload and parse an XML file first.")
            return

        self.log_message("Calculating statistics...")

        success, stats, error = self.data_controller.calculate_statistics()

        if success:
            self.log_message("✓ Statistics calculated successfully!")
            self.log_message(f"  Total users: {stats.get('total_users', 0)}")
            self.log_message(f"  Total posts: {stats.get('total_posts', 0)}")
            self.log_message(f"  Total followers: {stats.get('total_followers', 0)}")
            self.log_message(f"  Total following: {stats.get('total_following', 0)}")
            self.log_message(f"  Average followers per user: {stats.get('avg_followers', 0):.2f}")
            self.log_message(f"  Average posts per user: {stats.get('avg_posts', 0):.2f}")

            stats_text = (
                f"User Statistics:\n\n"
                f"Total Users: {stats.get('total_users', 0)}\n"
                f"Total Posts: {stats.get('total_posts', 0)}\n"
                f"Total Followers: {stats.get('total_followers', 0)}\n"
                f"Total Following: {stats.get('total_following', 0)}\n"
                f"Average Followers: {stats.get('avg_followers', 0):.2f}\n"
                f"Average Posts: {stats.get('avg_posts', 0):.2f}"
            )
            QMessageBox.information(self, "User Statistics", stats_text)
        else:
            self.log_message(f"✗ Statistics calculation failed: {error}")
            QMessageBox.critical(self, "Statistics Failed", f"Failed to calculate statistics:\n{error}")

    def export_to_json(self):
        """Export XML data to JSON format."""
        if not self.data_controller or not self.data_controller.xml_data:
            self.log_message("ERROR: No data loaded. Please upload and parse a file first.")
            QMessageBox.warning(self, "No Data", "Please upload and parse an XML file first.")
            return

        self.log_message("Exporting to JSON...")

        # Get save location from user
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            self.log_message("User cancelled JSON export.")
            return

        # Ensure .json extension
        if not file_path.endswith('.json'):
            file_path += '.json'

        success, message, error = self.data_controller.export_to_json(file_path)

        if success:
            self.log_message(f"✓ {message}")
            QMessageBox.information(self, "Export Success", message)
        else:
            self.log_message(f"✗ Export failed: {error}")
            QMessageBox.critical(self, "Export Failed", f"Failed to export to JSON:\n{error}")


