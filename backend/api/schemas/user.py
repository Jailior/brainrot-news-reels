"""
Pydantic schemas for user authentication and profile.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class UserLogin(BaseModel):
    """Login request schema."""
    email: str
    password: str


class UserSignup(BaseModel):
    """Signup request schema."""
    name: str
    email: str
    password: str


class SetupRequest(BaseModel):
    """Setup/preferences update request schema."""
    user_id: int
    preferences: Dict[str, Any]


class UserUpdateRequest(BaseModel):
    """User update request schema."""
    user_id: int
    name: Optional[str] = None
    password: Optional[str] = None
    current_password: Optional[str] = None


class DeleteAccountRequest(BaseModel):
    """Delete account request schema."""
    user_id: int


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    name: Optional[str] = None
    email: str
    has_completed_setup: bool = False
    preferences: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
