"""
Database connection and session management.

This module provides SQLAlchemy engine, session factory, and database initialization.
It handles connection pooling and provides a dependency for FastAPI routes to get
database sessions.

Interactions:
- Used by all model classes for database operations
- Used by all service classes via dependency injection
- Used by main.py for database initialization on startup
- Imports from config.py for database connection string
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from backend.config import settings

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20,
    echo=settings.debug,  # Log SQL queries in debug mode
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI routes to get database sessions.
    
    This function creates a database session, yields it to the route handler,
    and ensures it's properly closed after the request completes.
    
    Usage in FastAPI routes:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This function should be called on application startup to ensure all
    database tables exist. It creates tables based on the models defined
    in the models/ directory.
    
    Interactions:
        - Uses Base from this module (which all models inherit from)
        - Creates tables for: Article, Reel, Caption, BackgroundVideo, User
    """
    # Import all models to ensure they're registered with Base
    from backend.models.article import Article
    from backend.models.reel import Reel
    from backend.models.caption import Caption
    from backend.models.background_video import BackgroundVideo
    from backend.models.user import User
    
    # Create all tables
    Base.metadata.create_all(bind=engine)

