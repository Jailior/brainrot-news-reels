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
        country: Optional[str] = None,
        category: Optional[str] = None,
        page_size: int = 100,
    ) -> List[Dict]:
        """
        Fetch articles from NewsAPI.
        
        Args:
            country: Article country (e.g., 'us', 'gb') (optional)
            category: Article category (e.g., 'technology', 'sports') (optional)
            page_size: Number of articles to fetch (default: 10)
        
        Returns:
            List[Dict]: List of article dictionaries with fields:
                - title: Article headline
                - content: Article text
                - source: Source name
                - publishedAt: Publication timestamp
                - url: Original article URL
                - category: Article category
                - country: Article country
        
        Raises:
            requests.RequestException: If API call fails
            ValueError: If API key is not configured
        
        Interactions:
            - Called before save_articles() to get article data
            - Returns raw article data that will be saved to database
        """
        if not self.api_key:
            raise ValueError("NewsAPI key is not configured. Please set NEWSAPI_KEY environment variable.")
        
        # Determine which endpoint to use
        if category and country:
            endpoint = f"{self.base_url}/top-headlines"
            params = {
                "category": category,
                "pageSize": page_size,
                "country": country,
                "language": "en"
            }
        elif category:
            endpoint = f"{self.base_url}/top-headlines"
            params = {
                "pageSize": page_size,
                'category':category,
                "language": "en"
            }
        elif country:
            endpoint = f"{self.base_url}/top-headlines"
            params = {
                "pageSize": page_size,
                'country': country,
                "language": "en"
            }
        else:
            endpoint = f"{self.base_url}/top-headlines"
            params = {
                "pageSize": page_size,
                "language": "en"
            }

        
        # Make API request with authentication header
        headers = {
            "X-API-Key": self.api_key
        }
        
        try:
            response = requests.get(endpoint, params=params, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for bad status codes
            
            data = response.json()
            
            # Check if API returned an error
            if data.get("status") == "error":
                error_message = data.get("message", "Unknown error from NewsAPI")
                raise requests.RequestException(f"NewsAPI error: {error_message}")
            
            # Extract articles from response
            articles = data.get("articles", [])
            
            # Transform articles to match expected format
            formatted_articles = []
            for article in articles:
                content = article.get("content") or article.get("description") or ""
                if content and content.strip().endswith("…"):
                    content = content.strip()[:-1]
                
                title = article.get("title", "")
                source = article.get("source", {}).get("name", "Unknown")
                
                # Generate unique_id from title + source
                unique_id = self._generate_unique_id(title, source)
                
                formatted_article = {
                    "unique_id": unique_id,
                    "title": title,
                    "content": content,
                    "source": source,
                    "publishedAt": article.get("publishedAt"),
                    "url": article.get("url", ""),
                    "category": category
                }
                formatted_articles.append(formatted_article)
            
            return formatted_articles
            
        except requests.exceptions.Timeout:
            raise requests.RequestException("NewsAPI request timed out. Please try again later.")
        except requests.exceptions.HTTPError as e:
            raise requests.RequestException(f"NewsAPI HTTP error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to fetch articles from NewsAPI: {str(e)}")

    
    def _generate_unique_id(self, title: str, source: str) -> str:
        """
        Generate a unique identifier from title and source.
        
        Combines title and source with a separator for deduplication.
        
        Args:
            title: Article title
            source: Article source name
        
        Returns:
            str: Unique identifier (title + separator + source)
        """
        # Use || as separator to clearly distinguish title from source
        return f"{title}||{source}"
    
    def save_articles(self, articles: List[Dict], db: Session) -> List[Article]:
        """
        Save fetched articles to the database with deduplication.
        
        Checks for existing articles using unique_id (title + source) and
        only saves new articles that don't already exist.
        
        Args:
            articles: List of article dictionaries from fetch_articles()
            db: Database session for persistence
        
        Returns:
            List[Article]: List of newly saved Article model instances
        
        Raises:
            SQLAlchemyError: If database operation fails
        
        Interactions:
            - Creates Article instances and saves to database
            - Called after fetch_articles() to persist data
            - Skips duplicates based on unique_id
            - Returns Article objects that can be used by ScriptGenerator
        """
        saved_articles = []
        
        for article_dict in articles:
            unique_id = article_dict.get("unique_id")
            
            # Check if article already exists
            existing = db.query(Article).filter(Article.unique_id == unique_id).first()
            if existing:
                continue  # Skip duplicate
            
            # Parse publishedAt timestamp
            published_at_str = article_dict.get("publishedAt")
            try:
                if published_at_str:
                    # Parse ISO format: "2024-01-15T10:30:00Z"
                    timestamp = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
                else:
                    timestamp = datetime.utcnow()
            except (ValueError, AttributeError):
                timestamp = datetime.utcnow()
            
            # Create new Article instance
            new_article = Article(
                unique_id=unique_id,
                title=article_dict.get("title", ""),
                content=article_dict.get("content", ""),
                source=article_dict.get("source", "Unknown"),
                timestamp=timestamp,
                category=article_dict.get("category"),
                visited=False  # New articles start as unvisited
            )
            
            db.add(new_article)
            saved_articles.append(new_article)
        
        # Commit all new articles at once
        if saved_articles:
            db.commit()
            # Refresh to get IDs
            for article in saved_articles:
                db.refresh(article)
        
        return saved_articles
    
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
        return db.query(Article).filter(Article.id == article_id).first()
    
    def mark_article_visited(self, article_id: int, db: Session) -> Optional[Article]:
        """
        Mark an article as visited (processed by the pipeline).
        
        Args:
            article_id: Primary key of the article
            db: Database session
        
        Returns:
            Optional[Article]: Updated Article instance if found, None otherwise
        
        Interactions:
            - Called when pipeline starts processing an article
            - Sets visited=True to track which articles have been used
        """
        article = db.query(Article).filter(Article.id == article_id).first()
        if article:
            article.visited = True
            db.commit()
            db.refresh(article)
        return article
    
    def count_unused_articles(self, db: Session) -> int:
        """
        Count articles that haven't been visited yet (unused).
        
        Args:
            db: Database session
        
        Returns:
            int: Number of unvisited articles
        
        Interactions:
            - Used to determine when to fetch more articles
            - Returns count of articles with visited=False
        """
        return db.query(Article).filter(Article.visited == False).count()
    
    def count_visited_articles(self, db: Session) -> int:
        """
        Count articles that have been visited (used by pipeline).
        
        Args:
            db: Database session
        
        Returns:
            int: Number of visited articles
        
        Interactions:
            - Used for tracking/analytics
            - Returns count of articles with visited=True
        """
        return db.query(Article).filter(Article.visited == True).count()
    
    def get_next_unused_article(self, db: Session) -> Optional[Article]:
        """
        Get the next unused article (oldest unvisited article).
        
        Args:
            db: Database session
        
        Returns:
            Optional[Article]: Oldest unvisited article, or None if none available
        
        Interactions:
            - Used by pipeline to get next article to process
            - Returns article with visited=False, ordered by created_at ascending
        """
        return db.query(Article).filter(
            Article.visited == False
        ).order_by(Article.created_at.asc()).first()

