"""
XML Controller - Handles XML parsing, validation, and formatting operations.
"""

import xml.etree.ElementTree as ET
from typing import Optional
from xml.dom import minidom


class XMLController:
    """Controller for XML-related operations."""
    
    def __init__(self):
        self.xml_tree = None
        self.xml_data = None
        self.current_file_path = ""
        self.user_record_count = 0
    
    def parse_xml_file(self,
                       file_path: str
                       )-> tuple:
        """
        Parse an XML file and load the data.
        
        Args:
            file_path: Path to the XML file
            
        Returns:
            tuple: (success: bool, message: str, user_count: int)
        """
        try:
            self.xml_tree = ET.parse(file_path)
            self.xml_data = self.xml_tree.getroot()
            self.current_file_path = file_path
            self.user_record_count = len(self.xml_data.findall('.//user'))
            return True, f"File validated successfully. Found {self.user_record_count} user records.", self.user_record_count
        except ET.ParseError as e:
            return False, f"XML parsing failed: {str(e)}", 0
        except FileNotFoundError:
            return False, f"File not found: {file_path}", 0
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", 0
    
    def validate_xml_structure(self,
                               file_path: str
                               )-> tuple:
        """
        Validate XML structure.
        
        Args:
            file_path: Path to the XML file
            
        Returns:
            tuple: (success: bool, details: list, error: str | None)
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            users = root.findall('.//user')
            metadata = root.find('.//metadata')
            
            details = [f"✓ Root element: <{root.tag}>"]

            if metadata is not None:
                details.append("✓ Metadata section found")
            
            details.append(f"✓ Found {len(users)} user elements")
            
            valid_users = sum(1 for user in users if user.get('id'))
            details.append(f"✓ {valid_users} users have valid ID attributes")
            
            return True, details, None
        except ET.ParseError as e:
            return False, [], f"XML validation failed: {str(e)}"
        except Exception as e:
            return False, [], f"Validation error: {str(e)}"
    
    def format_xml_file(self,
                        file_path: str,
                        dest_path: Optional[str] = None
                        )-> tuple:
        """
        Format/prettify an XML file.
        
        Args:
            file_path: Path to the XML file
            dest_path: destination path for saving the XML
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Convert to string and pretty print
            rough_string = ET.tostring(root, encoding='unicode')
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="    ")
            
            # Remove extra blank lines and fix XML declaration
            lines = [line for line in pretty_xml.split('\n') if line.strip()]
            if not lines[0].startswith('<?xml'):
                lines.insert(0, '<?xml version="1.0" encoding="UTF-8"?>')
            elif 'encoding=' not in lines[0]:
                lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
            formatted_xml = '\n'.join(lines)

            if dest_path is None or "":
                dest_path = file_path
            # Save the formatted XML to destination path
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(formatted_xml)
            
            # Reload the XML data
            self.xml_tree = ET.parse(file_path)
            self.xml_data = self.xml_tree.getroot()
            self.user_record_count = len(self.xml_data.findall('.//user'))
            
            return True, f"XML file formatted successfully. File saved: {file_path}"
        except ET.ParseError as e:
            return False, f"XML parsing failed: {str(e)}"
        except Exception as e:
            return False, f"Failed to format XML: {str(e)}"
    
    def read_xml_file_content(self, file_path)-> tuple:
        """
        Read XML file content as text.
        
        Args:
            file_path: Path to the XML file
            
        Returns:
            tuple: (success: bool, content: str, error: str)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return True, content, None
        except FileNotFoundError:
            return False, "", f"File not found: {file_path}"
        except Exception as e:
            return False, "", f"Error reading file: {str(e)}"
    
    def get_xml_data(self):
        """Get the current XML data root element."""
        return self.xml_data
    
    def get_xml_tree(self):
        """Get the current XML tree."""
        return self.xml_tree

