"""
Script generator service for Claude API integration.

This service takes article text and generates engaging "brainrot" scripts
using Claude API. The generated scripts are saved to the reels table.

Interactions:
- Reads Article from database (via NewsFetcher.get_article_by_id)
- Calls Claude API to generate script
- Creates Reel record with generated script
- Uses config.py for Claude API key and model
- Saves script to database.reels.script field
"""

import requests
from typing import Optional
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.article import Article
from backend.models.reel import Reel, ReelStatus


class ScriptGenerator:
    """
    Service for generating "brainrot" scripts from articles using Claude API.
    
    This service takes article content and transforms it into engaging,
    viral-style scripts suitable for short-form video content.
    """
    
    def __init__(self):
        """
        Initialize the script generator with Claude API configuration.
        
        Uses settings from config.py for API key, base URL, and model.
        """
        self.api_key = settings.claude_api_key
        self.base_url = settings.claude_base_url
        self.model = settings.claude_model
    
    def generate_script(self, article: Article) -> str:
        """
        Generate a script from article content using Claude API.
        
        Args:
            article: Article model instance with title and content
        
        Returns:
            str: Generated "brainrot" script text
        
        Raises:
            requests.RequestException: If API call fails
            ValueError: If API key is not configured
        
        Interactions:
            - Called with Article object from database
            - Sends article.title and article.content to Claude API
            - Returns script text that will be saved to Reel.script
        """
        # TODO: Implement Claude API call
        # Use requests.post() to call Claude API endpoint
        # Include article.title and article.content in prompt
        # Request "brainrot" style script generation
        # Parse response and extract generated script text
        # Return script string
        pass
    
    def save_script(self, article_id: int, script: str, db: Session) -> Reel:
        """
        Save generated script to database in reels table.
        
        Args:
            article_id: ID of the article this script is based on
            script: Generated script text from generate_script()
            db: Database session
        
        Returns:
            Reel: Created Reel model instance with script saved
        
        Raises:
            SQLAlchemyError: If database operation fails
        
        Interactions:
            - Creates new Reel record linked to Article
            - Sets Reel.script field with generated text
            - Sets Reel.status to SCRIPT_GENERATED
            - Returns Reel object for use by AudioGenerator
        """
        # TODO: Implement script saving
        # Create new Reel instance
        # Set article_id, script, and status=ReelStatus.SCRIPT_GENERATED
        # Use db.add() and db.commit() to save
        # Return created Reel object
        pass
    
    def get_script_by_reel_id(self, reel_id: int, db: Session) -> Optional[str]:
        """
        Retrieve script text from database by reel ID.
        
        Args:
            reel_id: Primary key of the reel
            db: Database session
        
        Returns:
            Optional[str]: Script text if found, None otherwise
        
        Interactions:
            - Used by AudioGenerator to get script for TTS generation
            - Can be used by API endpoints to return script data
        """
        # TODO: Implement script retrieval
        # Use db.query(Reel).filter(Reel.id == reel_id).first()
        # Return Reel.script if found, None otherwise
        pass

