import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor


class LandingWindow(QWidget):
    """
    The initial window where the user selects the XML input method.
    """
    # Custom signal emitted when a button is clicked, carrying the input type
    navigation_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SocialNet XML Data Editor - Startup")
        self.setFixedSize(650, 450)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Optional: For a cleaner look
        self.setAttribute(Qt.WA_TranslucentBackground)  # Allows for shadow effects

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        # Main Layout (Centered Card)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # The central card widget for the content
        self.central_card = QWidget()
        self.central_card.setObjectName("CentralCard")

        # Add shadow effect to the central card for depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        self.central_card.setGraphicsEffect(shadow)

        # Card Content Layout
        card_layout = QVBoxLayout(self.central_card)
        card_layout.setSpacing(25)
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setAlignment(Qt.AlignCenter)

        # 1. Header (Matching Main App Identity)
        title_label = QLabel("SocialNet XML Data Editor")
        title_label.setObjectName("TitleLabel")

        icon_label = QLabel("🌐")
        icon_label.setObjectName("IconLabel")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setTextFormat(Qt.MarkdownText)
        icon_label.setText("## 🌐")  # Using a large emoji as a placeholder graphic

        subtitle_label = QLabel("How would you like to provide the XML input data?")
        subtitle_label.setObjectName("SubtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)

        # 2. Buttons
        self.btn_browse = self._create_button("Browse Local XML File", "📂")
        self.btn_manual = self._create_button("Enter XML Manually", "⌨️")

        # Link buttons to the signal emitter
        self.btn_browse.clicked.connect(lambda: self.navigation_requested.emit('browse'))
        self.btn_manual.clicked.connect(lambda: self.navigation_requested.emit('manual'))

        # 3. Footer
        version_label = QLabel("Version 1.X.X")
        version_label.setObjectName("VersionLabel")
        version_label.setAlignment(Qt.AlignCenter)

        # Add widgets to card layout
        card_layout.addWidget(icon_label)
        card_layout.addWidget(title_label)
        card_layout.addWidget(subtitle_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.btn_browse)
        card_layout.addWidget(self.btn_manual)
        card_layout.addSpacing(10)
        card_layout.addWidget(version_label)

        main_layout.addWidget(self.central_card)

    def _create_button(self, text, icon_text):
        btn = QPushButton(f"{icon_text}  {text}")
        btn.setFixedSize(300, 55)
        btn.setFont(QFont("Segoe UI", 12))
        return btn

    def apply_styles(self):
        # The QSS is designed to replicate the dark, connected network background
        # and the translucent card effect.
        style_sheet = """
        /* --- GLOBAL STYLES (Background & Window) --- */
        LandingWindow {
            /* Simulates the dark background with purple/blue glowing network nodes */
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #0F0F1A, stop:1 #1A1A2E);
        }

        /* --- CENTRAL CARD STYLING --- */
        #CentralCard {
            background-color: rgba(30, 30, 50, 0.9); /* Dark translucent blue */
            border: 2px solid rgba(74, 123, 167, 0.4); /* Subtle glow border */
            border-radius: 20px;
            padding: 30px;
        }

        /* --- TEXT STYLES --- */
        #TitleLabel {
            color: #4A7BA7; /* Matching the main app's header color */
            font-size: 24pt;
            font-weight: bold;
            margin-bottom: 5px;
        }
        #IconLabel {
            color: #7B90C9; /* Lighter purple/blue for the icon */
            font-size: 30pt;
        }
        #SubtitleLabel {
            color: #C0C0D0;
            font-size: 11pt;
            margin-bottom: 20px;
        }
        #VersionLabel {
            color: #5A5A70;
            font-size: 9pt;
        }

        /* --- BUTTON STYLES --- */
        QPushButton {
            border-radius: 10px;
            padding: 10px 20px;
            color: white;
            font-weight: 500;
            text-align: left;
        }

        /* Primary Button: Browse Local XML File (Blue/Active) */
        LandingWindow QPushButton:first-of-type { 
            background-color: #007ACC;
            border: 1px solid #005A99;
        }
        LandingWindow QPushButton:first-of-type:hover {
            background-color: #0099E6; /* Lighter on hover */
        }

        /* Secondary Button: Enter XML Manually (Dark/Subtle) */
        LandingWindow QPushButton:nth-child(2) {
            background-color: #3C3C3F;
            border: 1px solid #4A4A4A;
        }
        LandingWindow QPushButton:nth-child(2):hover {
            background-color: #4A4A4D;
        }
        """
        self.setStyleSheet(style_sheet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LandingWindow()
    window.show()
    sys.exit(app.exec())