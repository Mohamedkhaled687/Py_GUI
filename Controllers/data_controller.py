"""
Data Controller - Handles data operations like parsing, statistics, error checking, and JSON export.
"""

import json
from datetime import datetime
import xml.etree.ElementTree as ET


class DataController:
    """Controller for data-related operations."""
    
    def __init__(self, xml_data=None):
        self.xml_data = xml_data
    
    def set_xml_data(self, xml_data):
        """Set the XML data root element."""
        self.xml_data = xml_data
    
    def parse_user_data(self):
        """
        Parse user data and return statistics.
        
        Returns:
            tuple: (success: bool, stats: dict, error: str)
        """
        if self.xml_data is None:
            return False, {}, "No data loaded. Please upload and parse an XML file first."
        
        try:
            users = self.xml_data.findall('.//user')
            
            total_followers = 0
            total_following = 0
            total_posts = 0
            
            for user in users:
                followers = user.find('followers')
                following = user.find('following')
                posts = user.findall('.//post')
                
                if followers is not None and followers.text:
                    try:
                        total_followers += int(followers.text.strip())
                    except (ValueError, AttributeError):
                        pass
                if following is not None and following.text:
                    try:
                        total_following += int(following.text.strip())
                    except (ValueError, AttributeError):
                        pass
                total_posts += len(posts)
            
            # Get sample user info
            sample_user_info = {}
            if users:
                sample_user = users[0]
                user_id = sample_user.get('id', 'N/A')
                username = sample_user.find('username')
                username_text = username.text if username is not None else "N/A"
                sample_user_info = {"id": user_id, "username": username_text}
            
            stats = {
                "total_users": len(users),
                "total_followers": total_followers,
                "total_following": total_following,
                "total_posts": total_posts,
                "sample_user": sample_user_info
            }
            
            return True, stats, None
        except Exception as e:
            return False, {}, f"Error while parsing user data: {str(e)}"
    
    def check_for_errors(self):
        """
        Check for data integrity issues.
        
        Returns:
            tuple: (success: bool, errors: list, warnings: list, error_msg: str)
        """
        if self.xml_data is None:
            return False, [], [], "No data loaded. Please upload and parse an XML file first."
        
        try:
            users = self.xml_data.findall('.//user')
            errors = []
            warnings = []
            
            # Collect all valid user IDs for validation
            valid_user_ids = set()
            for user in users:
                user_id = user.get('id')
                if user_id is None:
                    id_elem = user.find('id')
                    if id_elem is not None:
                        user_id = id_elem.text
                if user_id:
                    valid_user_ids.add(str(user_id))
            
            for idx, user in enumerate(users, 1):
                # Get user ID - try different structures
                user_id = user.get('id')
                if user_id is None:
                    id_elem = user.find('id')
                    if id_elem is not None:
                        user_id = id_elem.text
                
                # Check for missing ID (required)
                if not user_id:
                    errors.append(f"User #{idx}: Missing user ID")
                    continue
                
                # Check for missing name (required)
                name_elem = user.find('name')
                if name_elem is None or not name_elem.text:
                    errors.append(f"User {user_id}: Missing name")
                
                # Check posts structure
                posts = user.findall('.//post')
                for post in posts:
                    post_id = post.get('id')
                    if not post_id:
                        warnings.append(f"User {user_id}: Post missing ID")
                
                # Check followers list structure
                followers_list = []
                # Structure 1: <followers><follower><id>V</id></follower></followers>
                followers_elem = user.find('followers')
                if followers_elem is not None:
                    for follower in followers_elem.findall('follower'):
                        follower_id_elem = follower.find('id')
                        if follower_id_elem is not None and follower_id_elem.text:
                            followers_list.append(follower_id_elem.text)
                
                # Structure 2: <connections><friend user_id="V"/></connections>
                connections_elem = user.find('connections')
                if connections_elem is not None:
                    for friend in connections_elem.findall('friend'):
                        friend_id = friend.get('user_id')
                        if friend_id:
                            followers_list.append(friend_id)
                
                # Validate follower IDs exist in the network
                for follower_id in followers_list:
                    if str(follower_id) not in valid_user_ids:
                        warnings.append(f"User {user_id}: Follower ID {follower_id} does not exist in network")
            
            return True, errors, warnings, None
        except Exception as e:
            return False, [], [], f"Error checking failed: {str(e)}"
    
    def calculate_statistics(self):
        """
        Calculate user statistics.
        
        Returns:
            tuple: (success: bool, stats: dict, error: str)
        """
        if self.xml_data is None:
            return False, {}, "No data loaded. Please upload and parse an XML file first."
        
        try:
            users = self.xml_data.findall('.//user')
            
            total_users = len(users)
            total_posts = 0
            total_followers = 0
            total_following = 0
            ages = []
            
            for user in users:
                posts = user.findall('.//post')
                total_posts += len(posts)
                
                followers = user.find('followers')
                if followers is not None and followers.text:
                    try:
                        total_followers += int(followers.text.strip())
                    except (ValueError, AttributeError):
                        pass
                
                following = user.find('following')
                if following is not None and following.text:
                    try:
                        total_following += int(following.text.strip())
                    except (ValueError, AttributeError):
                        pass
                
                age = user.find('age')
                if age is not None and age.text:
                    try:
                        ages.append(int(age.text.strip()))
                    except (ValueError, AttributeError):
                        pass
            
            avg_age = sum(ages) / len(ages) if ages else 0
            avg_followers = total_followers / total_users if total_users > 0 else 0
            avg_posts = total_posts / total_users if total_users > 0 else 0
            
            stats = {
                "total_users": total_users,
                "total_posts": total_posts,
                "total_followers": total_followers,
                "total_following": total_following,
                "avg_age": avg_age,
                "avg_followers": avg_followers,
                "avg_posts": avg_posts
            }
            
            return True, stats, None
        except Exception as e:
            return False, {}, f"Statistics error: {str(e)}"
    
    def export_to_json(self, file_path, current_file_path):
        """
        Export XML data to JSON format.
        
        Args:
            file_path: Path to save the JSON file
            current_file_path: Path of the source XML file
            
        Returns:
            tuple: (success: bool, message: str, error: str)
        """
        if self.xml_data is None:
            return False, "", "No data loaded. Please upload and parse an XML file first."
        
        try:
            users = self.xml_data.findall('.//user')
            
            # Convert XML to JSON structure - only id, name, posts, and followers list
            json_data = {
                "users": []
            }
            
            for user in users:
                # Get user ID
                user_id = user.get('id')
                if user_id is None:
                    id_elem = user.find('id')
                    if id_elem is not None:
                        user_id = id_elem.text
                
                if user_id is None:
                    continue
                
                # Get user name
                name_elem = user.find('name')
                user_name = name_elem.text.strip() if name_elem is not None and name_elem.text else None
                
                # Build user dict with only required fields
                user_dict = {
                    "id": user_id,
                    "name": user_name,
                    "posts": [],
                    "followers": []
                }
                
                # Add posts
                for post in user.findall('.//post'):
                    likes_elem = post.find('likes')
                    likes = 0
                    if likes_elem is not None and likes_elem.text:
                        try:
                            likes = int(likes_elem.text.strip())
                        except (ValueError, AttributeError):
                            likes = 0
                    
                    content_elem = post.find('content')
                    content = content_elem.text.strip() if content_elem is not None and content_elem.text else ""
                    
                    timestamp_elem = post.find('timestamp')
                    timestamp = timestamp_elem.text.strip() if timestamp_elem is not None and timestamp_elem.text else ""
                    
                    post_dict = {
                        "id": post.get('id'),
                        "content": content,
                        "timestamp": timestamp,
                        "likes": likes
                    }
                    user_dict["posts"].append(post_dict)
                
                # Add followers list - handle both XML structures
                # Structure 1: <followers><follower><id>V</id></follower></followers>
                followers_elem = user.find('followers')
                if followers_elem is not None:
                    for follower in followers_elem.findall('follower'):
                        follower_id_elem = follower.find('id')
                        if follower_id_elem is not None and follower_id_elem.text:
                            follower_id = follower_id_elem.text.strip()
                            user_dict["followers"].append(follower_id)
                
                # Structure 2: <connections><friend user_id="V"/></connections>
                connections_elem = user.find('connections')
                if connections_elem is not None:
                    for friend in connections_elem.findall('friend'):
                        friend_id = friend.get('user_id')
                        if friend_id:
                            user_dict["followers"].append(friend_id)
                
                json_data["users"].append(user_dict)
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Successfully exported {len(users)} users to JSON. File saved: {file_path}", None
        except Exception as e:
            return False, "", f"Failed to export to JSON: {str(e)}"

