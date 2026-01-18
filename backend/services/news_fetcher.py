"""
News fetcher service for NewsAPI integration.

This service fetches news articles from NewsAPI and saves them to the database.
It handles API calls, error handling, and database persistence.

Key Features:
- Fetches articles based on optional category and/or country filters
- When neither filter is provided, fetches all articles using /everything endpoint
- Automatically fetches more articles when unused articles drop below 10
- Extracts full article content from URLs using trafilatura (LLM-friendly extraction)
- Provides articles to ScriptGenerator for script generation

Interactions:
- Calls NewsAPI to fetch articles
- Extracts full content from article URLs using trafilatura
- Saves articles to database using Article model
- Used by generate endpoint to trigger article fetching
- Used by ScriptGenerator via get_next_unused_article() to get articles
- Uses config.py for NewsAPI key and base URL
"""

import requests
import time
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime

try:
    from trafilatura import fetch_url, extract
    from trafilatura.settings import use_config
    TRAFILATURA_AVAILABLE = True
except ImportError:
    # Fallback if trafilatura is not installed
    fetch_url = None
    extract = None
    use_config = None
    TRAFILATURA_AVAILABLE = False

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
        page_size: int = 1,
        extract_content: bool = True,
        delay_between_extractions: float = 0.5,
    ) -> List[Dict]:
        """
        Fetch articles from NewsAPI and optionally scrape full content from URLs.
        
        Args:
            country: Article country (e.g., 'us', 'gb') (optional)
            category: Article category (e.g., 'technology', 'sports') (optional)
            page_size: Number of articles to fetch (default: 100)
            extract_content: If True, scrape full content from article URLs (default: True)
            delay_between_extractions: Delay in seconds between content extractions (default: 0.5)
        
        Returns:
            List[Dict]: List of article dictionaries with fields:
                - title: Article headline
                - content: Article text (scraped full content if extract_content=True)
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
            - Scrapes full content from URLs if extract_content=True
            - Returns article data with enriched content that will be saved to database
        """
        if not self.api_key:
            raise ValueError("NewsAPI key is not configured. Please set NEWSAPI_KEY environment variable.")
        
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
            endpoint = f"{self.base_url}/everything"
            params = {
                "q": "news",
                "pageSize": page_size,
                "language": "en",
                "sortBy": "publishedAt"
            }

        headers = {
            "X-API-Key": self.api_key
        }
        
        try:
            response = requests.get(endpoint, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
        
            if data.get("status") == "error":
                error_message = data.get("message", "Unknown error from NewsAPI")
                raise requests.RequestException(f"NewsAPI error: {error_message}")
        
            articles = data.get("articles", [])
            
            formatted_articles = []
            for i, article in enumerate(articles):
                initial_content = article.get("content") or article.get("description") or ""
                if initial_content and initial_content.strip().endswith("…"):
                    initial_content = initial_content.strip()[:-1]
                
                title = article.get("title", "")
                source = article.get("source", {}).get("name", "Unknown")
                article_url = article.get("url", "")
                
                if extract_content and article_url:
                    full_content = self._extract_full_content(
                        url=article_url,
                        fallback_content=initial_content,
                        timeout=15
                    )
                    if len(full_content) > len(initial_content):
                        content = full_content
                    else:
                        content = initial_content
                else:
                    content = initial_content
                
                if extract_content and i > 0 and article_url:
                    time.sleep(delay_between_extractions)
                
                # Generate unique_id from title + source
                unique_id = self._generate_unique_id(title, source)
                
                formatted_article = {
                    "unique_id": unique_id,
                    "title": title,
                    "content": content,
                    "source": source,
                    "publishedAt": article.get("publishedAt"),
                    "url": article_url,
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
        return f"{title}__{source}"
    
    def _extract_full_content(self, url: str, fallback_content: str = "", timeout: int = 10) -> str:
        """
        Extract full article content from URL using trafilatura.
        
        Attempts to fetch and extract the main content from the article URL.
        Falls back to the provided fallback_content if extraction fails.
        
        Args:
            url: Article URL to extract content from
            fallback_content: Content to use if extraction fails (default: empty string)
            timeout: Request timeout in seconds (default: 10)
        
        Returns:
            str: Extracted full content, or fallback_content if extraction fails
        
        Interactions:
            - Uses trafilatura library for content extraction
            - Called by save_articles() to enrich article content
            - Handles errors gracefully to not break the pipeline
        """
        if not url or not url.strip():
            return fallback_content
        
        if not TRAFILATURA_AVAILABLE or fetch_url is None or extract is None:
            return fallback_content
        
        try:
            config = use_config()
            config.set("DEFAULT", "DOWNLOAD_TIMEOUT", str(timeout))
            config.set("DEFAULT", "EXTRACTION_TIMEOUT", str(timeout * 2))
            
            downloaded = fetch_url(url, config=config)
            if not downloaded:
                return fallback_content
        
            extracted = extract(
                downloaded,
                include_comments=False,
                include_tables=False,
                include_images=False,
                include_links=False,
                output_format='txt',
                config=config
            )
            
            if extracted and extracted.strip():
                content = extracted.strip()
                content = ' '.join(content.split())
                return content
            else:
                return fallback_content
                
        except Exception as e:
            print(f"Warning: Failed to extract content from {url[:50]}...: {str(e)}")
            return fallback_content
    
    def save_articles(
        self,
        articles: List[Dict],
        db: Session,
        extract_full_content: bool = False,
        delay_between_extractions: float = 0.5
    ) -> List[Article]:
        """
        Save fetched articles to the database with deduplication.
        
        Checks for existing articles using unique_id (title + source) and
        only saves new articles that don't already exist. Articles should already
        have full content scraped from fetch_articles(), but can optionally extract
        again if needed.
        
        Args:
            articles: List of article dictionaries from fetch_articles() (with scraped content)
            db: Database session for persistence
            extract_full_content: If True, extract full content from URLs again (default: False)
            delay_between_extractions: Delay in seconds between content extractions (default: 0.5)
        
        Returns:
            List[Article]: List of newly saved Article model instances
        
        Raises:
            SQLAlchemyError: If database operation fails
        
        Interactions:
            - Creates Article instances and saves to database
            - Called after fetch_articles() to persist data
            - Skips duplicates based on unique_id
            - Articles already contain scraped content from fetch_articles()
            - Returns Article objects that can be used by ScriptGenerator
        """
        saved_articles = []
        
        for i, article_dict in enumerate(articles):
            unique_id = article_dict.get("unique_id")
            
            existing = db.query(Article).filter(Article.unique_id == unique_id).first()
            if existing:
                continue 
            
            initial_content = article_dict.get("content", "")
            article_url = article_dict.get("url", "")
            
            if extract_full_content and article_url:
                full_content = self._extract_full_content(
                    url=article_url,
                    fallback_content=initial_content
                )
                if len(full_content) > len(initial_content):
                    final_content = full_content
                else:
                    final_content = initial_content
            else:
                final_content = initial_content
        
            if extract_full_content and i > 0 and article_url:
                time.sleep(delay_between_extractions)
            
            published_at_str = article_dict.get("publishedAt")
            try:
                if published_at_str:
                    timestamp = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
                else:
                    timestamp = datetime.utcnow()
            except (ValueError, AttributeError):
                timestamp = datetime.utcnow()
            
            # Create new Article instance
            new_article = Article(
                unique_id=unique_id,
                title=article_dict.get("title", ""),
                content=final_content,
                source=article_dict.get("source", "Unknown"),
                timestamp=timestamp,
                category=article_dict.get("category"),
                visited=False 
            )
            
            db.add(new_article)
            saved_articles.append(new_article)
        
        if saved_articles:
            db.commit()
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
        Mark an article as visited.
        
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
        Count articles that have been visited.
        
        Args:
            db: Database session
        
        Returns:
            int: Number of visited articles
        
        Interactions:
            - Used for tracking/analytics
            - Returns count of articles with visited=True
        """
        return db.query(Article).filter(Article.visited == True).count()
    
    def ensure_sufficient_articles(
        self,
        db: Session,
        min_threshold: int = 10,
        country: Optional[str] = None,
        category: Optional[str] = None,
    ) -> bool:
        """
        Ensure there are sufficient unused articles in the database.
        Automatically fetches more articles if unused count is below threshold.
        
        Args:
            db: Database session
            min_threshold: Minimum number of unused articles required (default: 10)
            country: Optional country filter for fetching
            category: Optional category filter for fetching
        
        Returns:
            bool: True if articles were fetched, False if sufficient articles already exist
        
        Interactions:
            - Checks count_unused_articles() to see if more articles are needed
            - Calls fetch_articles() and save_articles() if below threshold
            - Uses /everything endpoint (no filters) when neither country nor category provided
        """
        unused_count = self.count_unused_articles(db)
        
        if unused_count < min_threshold:
            # Fetch more articles using the same filters (or none for /everything)
            # Extract content during fetch so articles have full content
            try:
                articles = self.fetch_articles(
                    country=country,
                    category=category,
                    page_size=100,
                    extract_content=True  # Scrape content during auto-fetch
                )
                saved = self.save_articles(articles, db, extract_full_content=False)  # Already scraped
                return len(saved) > 0
            except Exception as e:
                # Log error but don't fail - pipeline can continue with existing articles
                print(f"Warning: Failed to auto-fetch articles: {e}")
                return False
        
        return False
    
    def get_next_unused_article(
        self,
        db: Session,
        auto_fetch: bool = True,
        country: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Optional[Article]:
        """
        Get the next unused article (oldest unvisited article).
        Optionally auto-fetches more articles if unused count is low.
        
        Args:
            db: Database session
            auto_fetch: If True, automatically fetches more articles if unused < 10 (default: True)
            country: Optional country filter for auto-fetching (if auto_fetch is True)
            category: Optional category filter for auto-fetching (if auto_fetch is True)
        
        Returns:
            Optional[Article]: Oldest unvisited article, or None if none available
        
        Interactions:
            - Used by pipeline to get next article to process
            - Automatically ensures sufficient articles before returning
            - Returns article with visited=False, ordered by created_at ascending
            - Can be used by ScriptGenerator to get articles for script generation
        """
        if auto_fetch:
            self.ensure_sufficient_articles(db, min_threshold=10, country=country, category=category)
        
        return db.query(Article).filter(
            Article.visited == False
        ).order_by(Article.created_at.asc()).first()

