"""
User database model.

Represents a user in the system, storing their profile information,
authentication details, and content preferences.
"""

from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base


class User(Base):
    """
    User model representing a registered user.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        email: Unique email address for authentication
        name: User's full name
        hashed_password: Hashed password for security
        is_active: Whether the user account is active
        has_completed_setup: Whether the user has finished the setup portal
        preferences: JSON field storing user preferences (categories, video style, etc.)
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    has_completed_setup = Column(Boolean, default=False)
    preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"
