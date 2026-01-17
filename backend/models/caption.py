"""
Caption database model.

Represents word-level captions with timestamps for video reels. Captions are
generated using Whisper transcription to get exact word timing, then used to
create SRT subtitle files for video composition.

Interactions:
- Many-to-one relationship with Reel (many captions belong to one reel)
- Created by AudioGenerator service after extracting word timestamps from Whisper
- Read by VideoCompositor service to generate SRT subtitle files
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from typing import Optional

from backend.database import Base


class Caption(Base):
    """
    Caption model representing word-level captions with timestamps.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        reel_id: Foreign key to Reel that this caption belongs to
        text: The caption text (word or phrase)
        start_time: Start time in seconds (float for precision)
        end_time: End time in seconds (float for precision)
        sequence_order: Order of this caption in the sequence (for sorting)
        created_at: Timestamp when caption was created
        reel: Relationship to the parent Reel
    """
    
    __tablename__ = "captions"
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    reel_id = Column(Integer, ForeignKey("reels.id"), nullable=False, index=True)
    text = Column(String(200), nullable=False)
    start_time = Column(Float, nullable=False)  # Start time in seconds
    end_time = Column(Float, nullable=False)  # End time in seconds
    sequence_order = Column(Integer, nullable=False, index=True)  # For ordering captions
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationship: Many captions belong to one reel
    reel: Optional["Reel"] = relationship(
        "Reel",
        back_populates="captions",
    )
    
    def __repr__(self) -> str:
        """String representation of Caption."""
        return f"<Caption(id={self.id}, text='{self.text}', start={self.start_time}, end={self.end_time})>"

