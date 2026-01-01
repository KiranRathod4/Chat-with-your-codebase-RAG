"""
Sample Python module for testing code parsing
"""

import os
from typing import List, Optional

# Global constant
SECRET_KEY = "supersecret123"


def authenticate_user(token: str) -> bool:
    """
    Validates a JWT token and returns authentication status.
    
    Args:
        token: JWT token string
        
    Returns:
        True if token is valid, False otherwise
    """
    try:
        payload = decode_token(token)
        return payload is not None
    except Exception:
        return False


def decode_token(token: str) -> Optional[dict]:
    """Decodes a JWT token and returns the payload."""
    # Simplified decoding logic
    return {"user_id": 123}


class UserManager:
    """Manages user operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_user(self, user_id: int):
        """Retrieve user by ID"""
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")
    
    def create_user(self, username: str, email: str) -> bool:
        """
        Create a new user in the database.
        
        Returns:
            True if successful
        """
        return self.db.execute(
            f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')"
        )


def calculate_total(items: List[dict]) -> float:
    """Calculate total price from list of items"""
    return sum(item['price'] for item in items)