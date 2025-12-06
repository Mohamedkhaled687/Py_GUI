"""
Graph Visualization Window - UI component for displaying network graphs.
"""

from typing import Optional, Dict, List, Tuple
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx


class GraphVisualizationWindow(QWidget):
    """Window for visualizing network graphs."""
    
    def __init__(self, nodes: Dict[str, str], edges: List[Tuple[str, str]], 
                 main_window_size: QSize, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.nodes: Dict[str, str] = nodes
        self.edges: List[Tuple[str, str]] = edges
        self.main_window_size: QSize = main_window_size
        self.figure: Optional[Figure] = None
        self.canvas: Optional[FigureCanvas] = None
        self.setup_ui()
        self.draw_graph()
    
    def setup_ui(self) -> None:
        self.setWindowTitle("Social Network Graph Visualization")
        # Set the same size as the main window
        self.resize(self.main_window_size)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #2d4a6a; border-bottom: 1px solid #1a2f4a;")
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        title_label = QLabel("Social Network Graph - Directed Graph Visualization")
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        info_label = QLabel(f"Nodes: {len(self.nodes)} | Edges: {len(self.edges)}")
        info_label.setStyleSheet("color: white; font-size: 12px;")
        title_layout.addWidget(info_label)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        # Matplotlib figure and canvas
        self.figure = Figure(figsize=(10, 7), facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(title_bar)
        layout.addWidget(self.canvas)
    
    def draw_graph(self) -> None:
        """Draw the directed graph using networkx and matplotlib."""
        # Clear the figure
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes
        for node_id in self.nodes.keys():
            G.add_node(str(node_id))
        
        # Add edges (U → V means U follows V)
        for from_id, to_id in self.edges:
            G.add_edge(str(from_id), str(to_id))
        
        if len(G.nodes()) == 0:
            ax.text(0.5, 0.5, 'No nodes to display', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14)
            self.canvas.draw()
            return
        
        # Use spring layout for better visualization
        try:
            pos = nx.spring_layout(G, k=1, iterations=50, seed=42)
        except:
            # Fallback to circular layout if spring layout fails
            pos = nx.circular_layout(G)
        
        # Draw edges (arrows)
        nx.draw_networkx_edges(G, pos, ax=ax, 
                              arrows=True, arrowsize=20, 
                              edge_color='gray', width=1.5,
                              alpha=0.6, arrowstyle='->')
        
        # Draw nodes (circles)
        nx.draw_networkx_nodes(G, pos, ax=ax,
                              node_color='steelblue', 
                              node_size=1000,
                              alpha=0.9)
        
        # Draw labels
        labels = {str(node_id): str(node_id) for node_id in self.nodes.keys()}
        nx.draw_networkx_labels(G, pos, labels, ax=ax, 
                               font_size=10, font_weight='bold',
                               font_color='white')
        
        # Set title and remove axes
        ax.set_title(f"Social Network Graph ({len(G.nodes())} nodes, {len(G.edges())} edges)",
                    fontsize=14, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Refresh canvas
        self.canvas.draw()

