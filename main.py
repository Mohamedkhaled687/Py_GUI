"""
SocialNet XML Parser - Main Entry Point

This application parses and visualizes social network XML data.
The code is organized following OOP principles with separation of concerns:
- Controllers: Business logic (XML, Data, Graph operations)
- UI: User interface components (MainWindow, CodeViewerWindow, GraphVisualizationWindow)
"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
