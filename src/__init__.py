"""
SocialNet Parser - A social network XML data parser and visualizer.

This package provides functionality to parse, validate, format, and visualize
social network data stored in XML format.
"""

__version__ = "1.0.0"
__author__ = "SocialNet Parser Team"

from .controllers import XMLController, DataController, GraphController
from .ui import CodeViewerWindow, GraphVisualizationWindow
from .utilities import (
    read_file, write_file, read_binary, write_binary, pretty_format,
    is_opening_tag, is_closing_tag, extract_tag_name, tokenize
)

__all__ = [
    'XMLController',
    'DataController',
    'GraphController',
    'CodeViewerWindow',
    'GraphVisualizationWindow',
    'read_file',
    'write_file',
    'read_binary',
    'write_binary',
    'pretty_format',
    'is_opening_tag',
    'is_closing_tag',
    'extract_tag_name',
    'tokenize',
]
