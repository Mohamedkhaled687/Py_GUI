"""
SocialNet Parser - A social network XML data parser and visualizer.

This package provides functionality to parse, validate, format, and visualize
social network data stored in XML format.
"""

__version__ = "1.0.0"
__author__ = "SocialNet Parser Team"

from .controllers import XMLController, DataController, GraphController
from .ui import MainWindow, CodeViewerWindow, GraphVisualizationWindow

__all__ = [
    'XMLController',
    'DataController',
    'GraphController',
    'MainWindow',
    'CodeViewerWindow',
    'GraphVisualizationWindow',
]

