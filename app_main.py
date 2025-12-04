import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel)
from PySide6.QtCore import Qt
from src.ui.landing_window import LandingWindow
from src.ui.manual_mode import MainWindow as ManualModeWindow
from src.ui.browse_mode import MainWindow as BrowseModeWindow

# --- Application Manager Class for Flow Control ---
class AppManager:
    """
    Manages the application flow, specifically the transition between the
    LandingWindow and the MainWindow.
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.landing_window = LandingWindow()
        self.main_window = None

        # Connect the signal from the landing page to the transition slot
        self.landing_window.navigation_requested.connect(self.show_main_app)

        # Start by showing the initial landing page
        self.landing_window.show()

    def show_main_app(self, input_mode):
        """
        Slot triggered by the LandingWindow's signal.
        Handles the transition and input mode setting.
        """
        # 1. Hide the current (landing) window
        self.landing_window.hide()

        # 2. Handle specific input modes (e.g., show a manual input modal first)
        if input_mode == 'manual':
            # In a real app, you'd show a QDialog here to get the XML text
            print("Action: User chose Manual Input. (Manual input modal/logic would be triggered here)")
            # For simplicity, we skip the modal and launch the main window
            self.main_window = ManualModeWindow()
        elif input_mode == 'browse':
            print("Action: User chose Browse File. (File dialog would be shown in the Main Window)")
            self.main_window = BrowseModeWindow()

        self.main_window.show()

    def run(self):
        """Starts the Qt event loop."""
        sys.exit(self.app.exec())


if __name__ == '__main__':
    manager = AppManager()
    manager.run()