"""
Main Window - Main UI component for the SocialNet XML Parser application.
"""

from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QFileDialog, QMessageBox)
from PySide6.QtCore import Qt

from Controllers.xml_controller import XMLController
from Controllers.data_controller import DataController
from Controllers.graph_controller import GraphController
from UI.code_viewer_window import CodeViewerWindow
from UI.graph_visualization_window import GraphVisualizationWindow


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize controllers
        self.xml_controller = XMLController()
        self.data_controller = DataController()
        self.graph_controller = GraphController()
        
        # UI state
        self.current_file_path = ""
        self.user_record_count = 0
        
        self.setup_ui()
        self.apply_stylesheet()
        self.log_message("Application initialized.")
        self.log_message("Ready to load XML file.")
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("🌐 SocialNet XML Parser")
        self.setMinimumSize(1000, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left panel
        left_layout = QVBoxLayout()
        
        # Load XML Data Group
        load_group = QGroupBox("Load XML Data")
        load_group.setObjectName("loadGroup")
        load_layout = QVBoxLayout()
        
        file_label = QLabel("Select Social Network User Data File (XML)")
        file_label.setStyleSheet("color: #333; font-size: 13px; margin-bottom: 5px;")
        
        file_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("/path/to/your/file.xml")
        self.file_path_edit.setMinimumHeight(35)
        
        self.browse_btn = QPushButton("📁 Browse")
        self.browse_btn.setObjectName("browseBtn")
        self.browse_btn.setMinimumHeight(35)
        self.browse_btn.setMinimumWidth(100)
        self.browse_btn.clicked.connect(self.browse_file)
        
        self.upload_btn = QPushButton("⬆ Upload & Parse")
        self.upload_btn.setObjectName("uploadBtn")
        self.upload_btn.setMinimumHeight(35)
        self.upload_btn.setMinimumWidth(150)
        self.upload_btn.clicked.connect(self.upload_and_parse)
        
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_btn)
        file_layout.addWidget(self.upload_btn)
        
        load_layout.addWidget(file_label)
        load_layout.addSpacing(5)
        load_layout.addLayout(file_layout)
        load_group.setLayout(load_layout)
        
        # Operation Log Group
        log_group = QGroupBox("Operation Log")
        log_group.setObjectName("logGroup")
        log_layout = QVBoxLayout()
        
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setMinimumHeight(300)
        
        log_layout.addWidget(self.log_text_edit)
        log_group.setLayout(log_layout)
        
        left_layout.addWidget(load_group)
        left_layout.addWidget(log_group)
        left_layout.setStretch(1, 1)
        
        # Right panel - Operations
        ops_group = QGroupBox("Operations")
        ops_group.setObjectName("opsGroup")
        ops_group.setMaximumWidth(230)
        ops_layout = QVBoxLayout()
        
        # Parsing & Validation section
        parse_label = QLabel("Parsing & Validation")
        parse_label.setStyleSheet("font-weight: bold; color: white; margin-top: 10px; margin-bottom: 5px;")
        
        self.validate_btn = QPushButton("📋 Validate XML Structure")
        self.validate_btn.setObjectName("operationBtn")
        self.validate_btn.setMinimumHeight(40)
        self.validate_btn.clicked.connect(self.validate_xml)
        
        self.parse_btn = QPushButton("⚙ Parse User Data")
        self.parse_btn.setObjectName("operationBtn")
        self.parse_btn.setMinimumHeight(40)
        self.parse_btn.clicked.connect(self.parse_user_data)
        
        self.error_btn = QPushButton("⚠ Check for Errors")
        self.error_btn.setObjectName("operationBtn")
        self.error_btn.setMinimumHeight(40)
        self.error_btn.clicked.connect(self.check_for_errors)
        
        self.format_btn = QPushButton("✨ Format XML")
        self.format_btn.setObjectName("operationBtn")
        self.format_btn.setMinimumHeight(40)
        self.format_btn.clicked.connect(self.format_xml)
        
        self.code_btn = QPushButton("📝 View Code")
        self.code_btn.setObjectName("operationBtn")
        self.code_btn.setMinimumHeight(40)
        self.code_btn.clicked.connect(self.view_code)
        
        # Visualization section
        viz_label = QLabel("Visualization")
        viz_label.setStyleSheet("font-weight: bold; color: white; margin-top: 15px; margin-bottom: 5px;")
        
        self.visualize_btn = QPushButton("🔗 Visualize Network Graph")
        self.visualize_btn.setObjectName("operationBtn")
        self.visualize_btn.setMinimumHeight(40)
        self.visualize_btn.clicked.connect(self.visualize_network)
        
        self.stats_btn = QPushButton("📊 Show User Statistics")
        self.stats_btn.setObjectName("operationBtn")
        self.stats_btn.setMinimumHeight(40)
        self.stats_btn.clicked.connect(self.show_user_stats)
        
        self.export_btn = QPushButton("📄 Export to JSON")
        self.export_btn.setObjectName("operationBtn")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.clicked.connect(self.export_to_json)
        
        ops_layout.addWidget(parse_label)
        ops_layout.addWidget(self.validate_btn)
        ops_layout.addWidget(self.parse_btn)
        ops_layout.addWidget(self.error_btn)
        ops_layout.addWidget(self.format_btn)
        ops_layout.addWidget(self.code_btn)
        ops_layout.addWidget(viz_label)
        ops_layout.addWidget(self.visualize_btn)
        ops_layout.addWidget(self.stats_btn)
        ops_layout.addWidget(self.export_btn)
        ops_layout.addStretch()
        ops_group.setLayout(ops_layout)
        
        # Add to main layout
        main_layout.addLayout(left_layout, 3)
        main_layout.addWidget(ops_group, 1)
    
    def apply_stylesheet(self):
        """Apply stylesheet to the window."""
        stylesheet = """
            QMainWindow {
                background-color: black;
            }
            
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: white;
                border: 2px solid #5a7a9b;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #4a6a8b;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            
            #loadGroup, #logGroup {
                background-color: #4a6a8b;
            }
            
            #opsGroup {
                background-color: #5a7a9b;
            }
            
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: black;
                font-size: 13px;
            }
            
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: black;
            }
            
            #browseBtn {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #browseBtn:hover {
                background-color: #1976D2;
            }
            
            #uploadBtn {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            
            #uploadBtn:hover {
                background-color: #45a049;
            }
            
            #operationBtn {
                background-color: #3d5a7a;
                color: white;
                border: 1px solid #2d4a6a;
                border-radius: 4px;
                font-size: 13px;
                text-align: left;
                padding-left: 15px;
            }
            
            #operationBtn:hover {
                background-color: #4d6a8a;
            }
            
            QPushButton:pressed {
                background-color: #2d4a6a;
            }
        """
        self.setStyleSheet(stylesheet)
    
    def log_message(self, message):
        """Log a message to the operation log."""
        timestamp = datetime.now().strftime("[%H:%M:%S %p]")
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
            self.log_message("ERROR: No file selected. Please browse and select an XML file.")
            QMessageBox.warning(self, "No File", "Please select an XML file first.")
            return
        
        self.log_message(f"User initiated upload and parse for: {file_path}")
        
        success, message, user_count = self.xml_controller.parse_xml_file(file_path)
        
        if success:
            self.current_file_path = file_path
            self.user_record_count = user_count
            
            # Update controllers with XML data
            xml_data = self.xml_controller.get_xml_data()
            self.data_controller.set_xml_data(xml_data)
            self.graph_controller.set_xml_data(xml_data)
            
            self.log_message(f"Loading file: {file_path}...")
            self.log_message(message)
            self.log_message("Parsing completed. Data ready for visualization.")
            
            QMessageBox.information(
                self, 
                "Success", 
                f"File loaded successfully!\n\nFound {user_count} user records.\nData is ready for operations."
            )
        else:
            self.log_message(f"ERROR: {message}")
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{message}")
    
    def validate_xml(self):
        """Validate XML structure."""
        self.log_message("User requested XML structure validation.")
        
        if not self.current_file_path:
            self.log_message("ERROR: No file loaded. Please upload a file first.")
            QMessageBox.warning(self, "No File", "Please load an XML file first using 'Upload & Parse'.")
            return
        
        self.log_message("Validating XML structure...")
        
        success, details, error = self.xml_controller.validate_xml_structure(self.current_file_path)
        
        if success:
            self.log_message("XML structure validation completed successfully.")
            for detail in details:
                self.log_message(f"  {detail}")
            
            QMessageBox.information(
                self, 
                "Validation Success", 
                "XML structure is valid!\n\n" + "\n".join(details)
            )
        else:
            self.log_message(f"✗ Validation error: {error}")
            QMessageBox.critical(self, "Error", f"Validation error:\n{error}")
    
    def parse_user_data(self):
        """Parse user data and display statistics."""
        self.log_message("User requested detailed user data parsing.")
        
        success, stats, error = self.data_controller.parse_user_data()
        
        if not success:
            self.log_message(f"ERROR: {error}")
            QMessageBox.warning(self, "No Data", error)
            return
        
        self.log_message("Parsing user data in detail...")
        self.log_message(f"Processing {stats['total_users']} user records...")
        self.log_message(f"✓ Total followers across all users: {stats['total_followers']}")
        self.log_message(f"✓ Total following across all users: {stats['total_following']}")
        self.log_message(f"✓ Total posts found: {stats['total_posts']}")
        
        if stats.get('sample_user'):
            sample = stats['sample_user']
            self.log_message(f"Sample user - ID: {sample['id']}, Username: {sample['username']}")
        
        self.log_message("User data parsing completed successfully.")
        
        QMessageBox.information(
            self,
            "Parsing Complete",
            f"Successfully parsed {stats['total_users']} users!\n\n"
            f"Total Followers: {stats['total_followers']}\n"
            f"Total Following: {stats['total_following']}\n"
            f"Total Posts: {stats['total_posts']}"
        )
    
    def check_for_errors(self):
        """Check for data integrity errors."""
        self.log_message("User initiated error checking.")
        
        success, errors, warnings, error_msg = self.data_controller.check_for_errors()
        
        if not success:
            self.log_message(f"ERROR: {error_msg}")
            QMessageBox.warning(self, "No Data", error_msg)
            return
        
        self.log_message("Checking for data integrity issues...")
        
        if not errors and not warnings:
            xml_data = self.data_controller.xml_data
            user_count = len(xml_data.findall('.//user')) if xml_data else 0
            self.log_message("✓ No errors found. Data integrity verified.")
            self.log_message(f"✓ All {user_count} user records passed validation.")
            QMessageBox.information(
                self,
                "No Errors Found",
                f"Data integrity check completed!\n\n"
                f"✓ No errors found\n"
                f"✓ {user_count} users validated successfully"
            )
        else:
            if errors:
                self.log_message(f"✗ Found {len(errors)} error(s):")
                for error in errors[:5]:
                    self.log_message(f"  - {error}")
            
            if warnings:
                self.log_message(f"⚠ Found {len(warnings)} warning(s):")
                for warning in warnings[:5]:
                    self.log_message(f"  - {warning}")
            
            msg = ""
            if errors:
                msg += f"Errors: {len(errors)}\n" + "\n".join(errors[:5])
            if warnings:
                if msg:
                    msg += "\n\n"
                msg += f"Warnings: {len(warnings)}\n" + "\n".join(warnings[:5])
            
            QMessageBox.warning(self, "Issues Found", msg)
    
    def visualize_network(self):
        """Visualize the network graph."""
        self.log_message("User requested network graph visualization.")
        
        success, nodes, edges, error = self.graph_controller.build_graph()
        
        if not success:
            self.log_message(f"ERROR: {error}")
            QMessageBox.warning(self, "No Data", error)
            return
        
        self.log_message("Analyzing network connections...")
        self.log_message(f"✓ Found {len(nodes)} nodes (users) in the network")
        self.log_message(f"✓ Found {len(edges)} edges (connections)")
        
        # Create and show graph visualization window
        graph_window = GraphVisualizationWindow(nodes, edges, self.size(), self)
        graph_window.show()
        
        self.log_message("✓ Network graph visualization window opened.")
    
    def show_user_stats(self):
        """Show user statistics."""
        self.log_message("User requested user statistics.")
        
        success, stats, error = self.data_controller.calculate_statistics()
        
        if not success:
            self.log_message(f"ERROR: {error}")
            QMessageBox.warning(self, "No Data", error)
            return
        
        self.log_message("Calculating user statistics...")
        self.log_message(f"✓ Total Users: {stats['total_users']}")
        self.log_message(f"✓ Total Posts: {stats['total_posts']}")
        self.log_message(f"✓ Average Followers per User: {stats['avg_followers']:.1f}")
        self.log_message(f"✓ Average Age: {stats['avg_age']:.1f} years")
        self.log_message(f"✓ Average Posts per User: {stats['avg_posts']:.1f}")
        
        stats_text = (
            f"User Statistics Report\n"
            f"{'=' * 40}\n\n"
            f"Total Users: {stats['total_users']}\n"
            f"Total Posts: {stats['total_posts']}\n"
            f"Total Followers: {stats['total_followers']}\n"
            f"Total Following: {stats['total_following']}\n\n"
            f"Averages:\n"
            f"  - Posts per User: {stats['avg_posts']:.1f}\n"
            f"  - Followers per User: {stats['avg_followers']:.1f}\n"
            f"  - Age: {stats['avg_age']:.1f} years\n"
        )
        
        QMessageBox.information(self, "User Statistics", stats_text)
    
    def export_to_json(self):
        """Export data to JSON format."""
        self.log_message("User requested JSON export.")
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "social_network_export.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            self.log_message("User cancelled JSON export.")
            return
        
        self.log_message(f"Exporting data to JSON: {file_path}")
        
        success, message, error = self.data_controller.export_to_json(file_path, self.current_file_path)
        
        if success:
            self.log_message(f"✓ {message}")
            QMessageBox.information(
                self,
                "Export Successful",
                f"Data exported successfully!\n\n{message}"
            )
        else:
            self.log_message(f"ERROR: {error}")
            QMessageBox.critical(self, "Export Error", f"Failed to export to JSON:\n{error}")
    
    def format_xml(self):
        """Format/prettify the XML file."""
        self.log_message("User requested XML formatting.")
        
        if not self.current_file_path:
            self.log_message("ERROR: No file loaded. Please upload a file first.")
            QMessageBox.warning(self, "No File", "Please load an XML file first using 'Upload & Parse'.")
            return
        
        self.log_message(f"Formatting XML file: {self.current_file_path}")
        
        success, message = self.xml_controller.format_xml_file(self.current_file_path)
        
        if success:
            # Reload XML data after formatting
            xml_data = self.xml_controller.get_xml_data()
            self.data_controller.set_xml_data(xml_data)
            self.graph_controller.set_xml_data(xml_data)
            self.user_record_count = self.xml_controller.user_record_count
            
            self.log_message(f"✓ {message}")
            QMessageBox.information(
                self,
                "Format Successful",
                f"XML file formatted successfully!\n\n"
                f"File: {self.current_file_path}\n"
                f"The XML is now well-formatted with proper indentation."
            )
        else:
            self.log_message(f"ERROR: {message}")
            QMessageBox.critical(self, "Format Error", f"Failed to format XML:\n{message}")
    
    def view_code(self):
        """View XML code in a read-only window."""
        self.log_message("User requested to view code.")
        
        if not self.current_file_path:
            self.log_message("ERROR: No file loaded. Please upload a file first.")
            QMessageBox.warning(self, "No File", "Please load an XML file first using 'Upload & Parse'.")
            return
        
        success, content, error = self.xml_controller.read_xml_file_content(self.current_file_path)
        
        if success:
            self.log_message(f"Loading XML content from: {self.current_file_path}")
            code_viewer = CodeViewerWindow(content, self.size(), self)
            code_viewer.show()
            self.log_message("Code viewer window opened.")
        else:
            self.log_message(f"ERROR: {error}")
            QMessageBox.critical(self, "File Error", f"Error reading file:\n{error}")

