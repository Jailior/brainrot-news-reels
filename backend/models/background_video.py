"""
BackgroundVideo database model.

Represents background video files stored in S3. These videos are used as the
visual background for composited reels. Multiple background videos can be
uploaded, and one is randomly selected for each reel.

Interactions:
- Read by VideoCompositor service to get random background video URL
- Created manually or via admin script when uploading background videos to S3
- Only stores metadata (URL, name, duration) - actual video files are in S3
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, func
from typing import Optional

from backend.database import Base


class BackgroundVideo(Base):
    """
    BackgroundVideo model representing background video files in S3.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        name: Descriptive name for the background video
        s3_url: S3 URL to the background video file (MP4)
        duration: Duration of the video in seconds (for reference)
        created_at: Timestamp when this record was created
    """
    
    __tablename__ = "background_videos"
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    s3_url = Column(String(500), nullable=False, unique=True)
    duration = Column(Float, nullable=True)  # Duration in seconds, nullable if unknown
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        """String representation of BackgroundVideo."""
        return f"<BackgroundVideo(id={self.id}, name='{self.name}', url='{self.s3_url[:50]}...')>"

