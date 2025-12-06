"""
Graph Controller - Handles graph building and network analysis operations.
"""

import xml.etree.ElementTree as ET
from typing import Optional, Tuple, Dict, List


class GraphController:
    """Controller for graph-related operations."""
    
    def __init__(self, xml_data: Optional[ET.Element] = None) -> None:
        self.xml_data: Optional[ET.Element] = xml_data
    
    def set_xml_data(self, xml_data: Optional[ET.Element]) -> None:
        """Set the XML data root element."""
        self.xml_data = xml_data
    
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
            
            return True, nodes, edges, None
        except Exception as e:
            return False, {}, [], f"Error building graph: {str(e)}"

