"""
Pydantic schemas for Reel API requests and responses.

These schemas define the structure of API request/response data for reel endpoints.
They provide automatic validation and serialization of data.

Interactions:
- Used by reels.py routes for request/response validation
- Used by generate.py route for response formatting
- Automatically validates incoming request data
- Serializes database models to JSON responses
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReelResponse(BaseModel):
    """
    Response schema for a single reel.
    
    This schema represents a reel as returned to the frontend.
    Contains all necessary information for displaying a reel in the app.
    
    Fields:
        id: Unique reel identifier
        video_url: S3 URL to the final video file
        script: Generated script text
        views: Number of times reel has been viewed
        created_at: Timestamp when reel was created
    """
    
    id: int
    video_url: Optional[str] = None
    script: Optional[str] = None
    views: int
    created_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Allows conversion from SQLAlchemy models


class ReelListResponse(BaseModel):
    """
    Response schema for paginated list of reels.
    
    This schema wraps a list of reels with pagination metadata.
    Used by the GET /api/reels endpoint for infinite scroll.
    
    Fields:
        reels: List of ReelResponse objects
        total: Total number of reels available
        limit: Number of reels per page
        offset: Offset for pagination
    """
    
    reels: list[ReelResponse]
    total: int
    limit: int
    offset: int


class ReelDetailResponse(BaseModel):
    """
    Response schema for detailed reel information.
    
    Extended response that includes additional details like article information.
    Used by GET /api/reels/{id} endpoint.
    
    Fields:
        id: Unique reel identifier
        video_url: S3 URL to the final video file
        audio_url: S3 URL to the audio file
        script: Generated script text
        views: Number of times reel has been viewed
        status: Current processing status
        article_title: Title of source article
        created_at: Timestamp when reel was created
    """
    
    id: int
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    script: Optional[str] = None
    views: int
    status: str
    article_title: Optional[str] = None
    created_at: datetime
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ViewIncrementResponse(BaseModel):
    """
    Response schema for view increment endpoint.
    
    Simple response confirming view count was incremented.
    
    Fields:
        reel_id: ID of the reel
        views: Updated view count
    """
    
    reel_id: int
    views: int


class UserWatchedReelsResponse(BaseModel):
    """
    Response schema for user's watched reels endpoint.
    
    Returns a list of all reels that a user has watched.
    Used by GET /api/reels/users/{user_id}/watched endpoint.
    
    Fields:
        reels: List of ReelResponse objects that the user has watched
    """
    
    reels: list[ReelResponse]

