"""
ReelWatch database model.

Represents a watch history record tracking which users have watched which reels.
This is a junction table that creates a many-to-many relationship between
users and reels for watch history tracking.

Interactions:
- Many-to-one relationship with User (many watch records belong to one user)
- Many-to-one relationship with Reel (many watch records belong to one reel)
- Created when a user watches a reel (via view endpoint)
- Read by API routes to retrieve user's watch history
"""

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from typing import Optional

from backend.database import Base


class ReelWatch(Base):
    """
    ReelWatch model representing a user's watch history entry.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        user_id: Foreign key to User that watched the reel
        reel_id: Foreign key to Reel that was watched
        user: Relationship to the User
        reel: Relationship to the Reel
    """
    
    __tablename__ = "reel_watches"
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reel_id = Column(Integer, ForeignKey("reels.id"), nullable=False, index=True)
    
    # Composite unique constraint to prevent duplicate watch records
    __table_args__ = (
        UniqueConstraint('user_id', 'reel_id', name='uq_user_reel_watch'),
    )
    
    # Relationship: Many watch records belong to one user
    user: Optional["User"] = relationship(
        "User",
        backref="watched_reels",
    )
    
    # Relationship: Many watch records belong to one reel
    reel: Optional["Reel"] = relationship(
        "Reel",
        backref="watched_by_users",
    )
    
    def __repr__(self) -> str:
        """String representation of ReelWatch."""
        return f"<ReelWatch(id={self.id}, user_id={self.user_id}, reel_id={self.reel_id})>"
