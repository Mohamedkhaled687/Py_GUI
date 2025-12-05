"""
Browse Mode Window - Load XML from file browser
"""
from .base_xml_window import BaseXMLWindow


class BrowseWindow(BaseXMLWindow):
    """Browse mode window for loading XML from files."""

    def __init__(self):
        super().__init__(
            window_title="🌐 SocialNet XML Parser - Browse Mode",
            mode_name="Browse mode"
        )
