"""
Graph Controller - Handles graph building and network analysis operations.
"""

import xml.etree.ElementTree as ET
from typing import Optional, Tuple, Dict, List
import networkx as nx
import numpy as np


class GraphController:
    """Controller for graph-related operations."""
    
    def __init__(self, xml_data: Optional[ET.Element] = None) -> None:
        self.xml_data: Optional[ET.Element] = xml_data
        self.G: Optional[nx.DiGraph] = None
        self.metrics: Dict = {}
    
    def set_xml_data(self, xml_data: Optional[ET.Element]) -> None:
        """Set the XML data root element."""
        self.xml_data = xml_data
        self.G = None
        self.metrics = {}
    
    def build_graph(self) -> Tuple[bool, Dict[str, str], List[Tuple[str, str]], Optional[str]]:
        """
        Build graph structure from XML data.
        
        Returns:
            tuple: (success: bool, nodes: dict, edges: list, error: str)
            nodes: {user_id: user_name}
            edges: [(from_id, to_id)] where from_id follows to_id
        """
        if self.xml_data is None:
            return False, {}, [], "No data loaded. Please upload and parse an XML file first."
        
        try:
            users = self.xml_data.findall('.//user')
            
            # Build graph: nodes and edges
            nodes = {}  # {user_id: user_name}
            edges = []  # [(from_id, to_id)] where from_id follows to_id
            
            for user in users:
                # Get user ID - try different possible structures
                user_id = user.get('id')
                if user_id is None:
                    id_elem = user.find('id')
                    if id_elem is not None:
                        user_id = id_elem.text
                
                if user_id is None:
                    continue
                
                # Get user name
                name_elem = user.find('name')
                user_name = name_elem.text if name_elem is not None else f"User {user_id}"
                nodes[user_id] = user_name
                
                # Get followers - handle both structures
                # Structure 1: <followers><follower><id>V</id></follower></followers>
                followers_elem = user.find('followers')
                if followers_elem is not None:
                    for follower in followers_elem.findall('follower'):
                        follower_id_elem = follower.find('id')
                        if follower_id_elem is not None and follower_id_elem.text:
                            follower_id = follower_id_elem.text.strip()
                            edges.append((user_id, follower_id))  # U → V (U follows V)
                
                # Structure 2: <connections><friend user_id="V"/></connections>
                connections_elem = user.find('connections')
                if connections_elem is not None:
                    for friend in connections_elem.findall('friend'):
                        friend_id = friend.get('user_id')
                        if friend_id:
                            edges.append((user_id, friend_id))  # U → V (U follows V)
            
            if len(nodes) == 0:
                return False, {}, [], "No users found in XML data."
            
            # Build NetworkX graph
            self.G = self._build_networkx_graph(nodes, edges)
            # Calculate metrics
            self.metrics = self._calculate_metrics(nodes)
            
            return True, nodes, edges, None
        except Exception as e:
            return False, {}, [], f"Error building graph: {str(e)}"
    
    def _build_networkx_graph(self, nodes: Dict[str, str], edges: List[Tuple[str, str]]) -> nx.DiGraph:
        """Build a NetworkX directed graph from nodes and edges."""
        G = nx.DiGraph()
        
        # Add all nodes
        for node_id, node_name in nodes.items():
            G.add_node(str(node_id), name=node_name)
        
        # Add all edges (from_id follows to_id means edge from from_id to to_id)
        for from_id, to_id in edges:
            if str(from_id) in G.nodes() and str(to_id) in G.nodes():
                G.add_edge(str(from_id), str(to_id))
        
        return G
    
    def _calculate_metrics(self, nodes: Dict[str, str]) -> Dict:
        """Calculate network metrics for analysis."""
        if self.G is None:
            return {}
        
        metrics = {}
        
        # Basic metrics
        metrics['num_nodes'] = self.G.number_of_nodes()
        metrics['num_edges'] = self.G.number_of_edges()
        metrics['density'] = nx.density(self.G)
        
        # Degree metrics (in-degree = followers, out-degree = following)
        in_degrees = dict(self.G.in_degree())
        out_degrees = dict(self.G.out_degree())
        
        metrics['avg_in_degree'] = np.mean(list(in_degrees.values())) if in_degrees else 0
        metrics['avg_out_degree'] = np.mean(list(out_degrees.values())) if out_degrees else 0
        
        # Most influential (most followers)
        if in_degrees:
            most_influential_id = max(in_degrees, key=in_degrees.get)
            metrics['most_influential'] = {
                'id': most_influential_id,
                'name': nodes.get(most_influential_id, 'Unknown'),
                'followers': in_degrees[most_influential_id]
            }
        
        # Most active (follows most people)
        if out_degrees:
            most_active_id = max(out_degrees, key=out_degrees.get)
            metrics['most_active'] = {
                'id': most_active_id,
                'name': nodes.get(most_active_id, 'Unknown'),
                'following': out_degrees[most_active_id]
            }
        
        # Store degree dictionaries for visualization
        metrics['in_degrees'] = in_degrees
        metrics['out_degrees'] = out_degrees
        
        return metrics
    
    def get_graph(self) -> Optional[nx.DiGraph]:
        """Get the NetworkX graph object."""
        return self.G
    
    def get_metrics(self) -> Dict:
        """Get the calculated network metrics."""
        return self.metrics

