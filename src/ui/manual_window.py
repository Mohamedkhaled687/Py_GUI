"""
Manual Mode Window - Load XML from manual input
"""
from .base_xml_window import BaseXMLWindow


class ManualWindow(BaseXMLWindow):
    """Manual mode window for loading XML from files."""

    def __init__(self):
        super().__init__(
            window_title="🌐 SocialNet XML Parser - Manual Mode",
            mode_name="Manual mode"
        )
