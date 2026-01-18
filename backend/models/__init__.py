"""
Database models package.

This package contains all SQLAlchemy model definitions for the application.
Models define the database schema and relationships between entities.

Models:
- Article: News articles fetched from NewsAPI
- Reel: Generated video reels linked to articles
- Caption: Word-level captions with timestamps for reels
- BackgroundVideo: Background video files stored in S3
- ReelWatch: Watch history tracking which users have watched which reels
"""

from backend.models.article import Article
from backend.models.reel import Reel
from backend.models.caption import Caption
from backend.models.background_video import BackgroundVideo
from backend.models.reel_watch import ReelWatch

__all__ = ["Article", "Reel", "Caption", "BackgroundVideo", "ReelWatch"]

