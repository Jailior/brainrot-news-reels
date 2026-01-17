"""
News fetcher service for NewsAPI integration.

This service fetches news articles from NewsAPI and saves them to the database.
It handles API calls, error handling, and database persistence.

Interactions:
- Calls NewsAPI to fetch articles
- Saves articles to database using Article model
- Used by generate endpoint to trigger article fetching
- Uses config.py for NewsAPI key and base URL
"""

import requests
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from backend.config import settings
from backend.models.article import Article


class NewsFetcher:
    """
    Service for fetching news articles from NewsAPI.
    
    This service handles communication with NewsAPI, processes the response,
    and saves articles to the database.
    """
    
    def __init__(self):
        """
        Initialize the news fetcher with API configuration.
        
        Uses settings from config.py for API key and base URL.
        """
        self.api_key = settings.newsapi_key
        self.base_url = settings.newsapi_base_url
    
    def fetch_articles(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        page_size: int = 10,
    ) -> List[Dict]:
        """
        Fetch articles from NewsAPI.
        
        Args:
            query: Search query string (optional)
            category: Article category (e.g., 'technology', 'sports') (optional)
            page_size: Number of articles to fetch (default: 10)
        
        Returns:
            List[Dict]: List of article dictionaries with fields:
                - title: Article headline
                - content: Article text
                - source: Source name
                - publishedAt: Publication timestamp
                - url: Original article URL
        
        Raises:
            requests.RequestException: If API call fails
            ValueError: If API key is not configured
        
        Interactions:
            - Called before save_articles() to get article data
            - Returns raw article data that will be saved to database
        """
        # TODO: Implement NewsAPI call
        # Use requests.get() to call NewsAPI endpoint
        # Handle authentication with apiKey parameter
        # Parse response JSON and extract articles
        # Return list of article dictionaries
        pass
    
    def save_articles(self, articles: List[Dict], db: Session) -> List[Article]:
        """
        Save fetched articles to the database.
        
        Args:
            articles: List of article dictionaries from fetch_articles()
            db: Database session for persistence
        
        Returns:
            List[Article]: List of saved Article model instances
        
        Raises:
            SQLAlchemyError: If database operation fails
        
        Interactions:
            - Creates Article model instances and saves to database
            - Called after fetch_articles() to persist data
            - Returns Article objects that can be used by ScriptGenerator
        """
        # TODO: Implement article saving
        # Create Article instances from article dictionaries
        # Parse timestamp from publishedAt field
        # Extract category if available
        # Use db.add() and db.commit() to save
        # Return list of saved Article objects
        pass
    
    def get_article_by_id(self, article_id: int, db: Session) -> Optional[Article]:
        """
        Retrieve an article from the database by ID.
        
        Args:
            article_id: Primary key of the article
            db: Database session
        
        Returns:
            Optional[Article]: Article instance if found, None otherwise
        
        Interactions:
            - Used by ScriptGenerator to get article content
            - Can be used by API endpoints to retrieve article details
        """
        # TODO: Implement article retrieval
        # Use db.query(Article).filter(Article.id == article_id).first()
        # Return Article instance or None
        pass

