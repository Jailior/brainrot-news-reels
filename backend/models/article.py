"""
Article database model.

Represents news articles fetched from NewsAPI. Articles are the source material
for generating reels. Each article can have multiple reels generated from it.

Interactions:
- One-to-many relationship with Reel (one article can have many reels)
- Created by NewsFetcher service when fetching from NewsAPI
- Read by ScriptGenerator service to generate scripts
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from typing import List, Optional

from backend.database import Base


class Article(Base):
    """
    Article model representing news articles from NewsAPI.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        title: Article headline/title
        content: Full article text content
        source: News source name (e.g., "BBC News", "CNN")
        timestamp: Original publication timestamp from NewsAPI
        category: Article category/topic (e.g., "technology", "sports")
        created_at: Timestamp when article was saved to database
        reels: Relationship to Reel objects generated from this article
    """
    
    __tablename__ = "articles"
    __allow_unmapped__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    source = Column(String(200), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    category = Column(String(50), nullable=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationship: One article can have many reels
    reels: List["Reel"] = relationship(
        "Reel",
        back_populates="article",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        """String representation of Article."""
        return f"<Article(id={self.id}, title='{self.title[:50]}...')>"

