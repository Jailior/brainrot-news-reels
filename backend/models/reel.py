"""
Reel database model.

Represents a generated video reel. A reel goes through multiple stages:
1. Script generation (status: 'script_generated')
2. Audio generation (status: 'audio_generated')
3. Video composition (status: 'ready')

Interactions:
- Many-to-one relationship with Article (many reels can come from one article)
- One-to-many relationship with Caption (one reel has many caption segments)
- Created by ScriptGenerator service after generating script
- Updated by AudioGenerator service with audio_url
- Updated by VideoCompositor service with video_url and status='ready'
- Read by API routes to serve reels to frontend
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from typing import Optional
import enum

from backend.database import Base


class ReelStatus(str, enum.Enum):
    """Enumeration of possible reel statuses."""
    SCRIPT_GENERATED = "script_generated"
    AUDIO_GENERATED = "audio_generated"
    VIDEO_COMPOSITED = "video_composited"
    READY = "ready"
    FAILED = "failed"


class Reel(Base):
    """
    Reel model representing a generated video reel.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        article_id: Foreign key to Article that this reel is based on
        script: Generated "brainrot" script text from Claude API
        audio_url: S3 URL to the generated audio file (MP3)
        video_url: S3 URL to the final composited video file (MP4)
        status: Current processing status of the reel
        views: Number of times this reel has been viewed
        created_at: Timestamp when reel was created
        article: Relationship to the source Article
        captions: Relationship to Caption objects for this reel
    """
    
    __tablename__ = "reels"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False, index=True)
    script = Column(Text, nullable=True)  # Nullable until script is generated
    audio_url = Column(String(500), nullable=True)  # S3 URL, set by AudioGenerator
    video_url = Column(String(500), nullable=True)  # S3 URL, set by VideoCompositor
    status = Column(
        SQLEnum(ReelStatus),
        default=ReelStatus.SCRIPT_GENERATED,
        nullable=False,
        index=True,
    )
    views = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationship: Many reels belong to one article
    article: Optional["Article"] = relationship(
        "Article",
        back_populates="reels",
    )
    
    # Relationship: One reel has many captions
    captions: list["Caption"] = relationship(
        "Caption",
        back_populates="reel",
        cascade="all, delete-orphan",
        order_by="Caption.sequence_order",
    )
    
    def __repr__(self) -> str:
        """String representation of Reel."""
        return f"<Reel(id={self.id}, status='{self.status}', views={self.views})>"

