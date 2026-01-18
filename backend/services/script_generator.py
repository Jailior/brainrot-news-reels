"""
Script generator service for OpenRouter API integration.

This service takes article text and generates engaging "brainrot" scripts
using Claude API. The generated scripts are saved to the reels table.

Interactions:
- Reads Article from database (via NewsFetcher.get_article_by_id)
- Calls Claude API to generate script
- Uses config.py for OpenRouter API key and model
- Saves script to temp folder
"""
import os
import requests

from backend.config import settings
from backend.models.article import Article
from backend.models.reel import Reel, ReelStatus

def get_json_headers():
    return {
        "Authorization": f"Bearer {settings.open_router_api_key}",
        "Content-Type": "application/json"
    }

def get_json_prompt(prompt):
    return {
        "role": "user",
        "content": prompt
    }

class ScriptGenerator:
    """
    Service for generating "brainrot" scripts from articles using OpenRouter API.
    
    This service takes article content and transforms it into engaging,
    viral-style scripts suitable for short-form video content.
    """
    
    def __init__(self):
        """
        Initialize the script generator with OpenRouter API configuration.
        
        Uses settings from config.py for API key, base URL, and model.
        """
        self.api_key = settings.open_router_api_key
        self.base_url = settings.openrouter_base_url
        self.model = settings.openrouter_model
    
    def generate_script(self, article: Article) -> str:
        """
        Generate a script from article content using OpenRouter API.
        
        Args:
            article: Article model instance with title and content
        
        Returns:
            str: Generated "brainrot" script text
        
        Raises:
            requests.RequestException: If API call fails
            ValueError: If API key is not configured
        
        Interactions:
            - Called with Article object from database
            - Sends article.title and article.content to OpenRouter API
            - Returns script text that will be saved to Reel.script
        """
        article_title = article.title
        article_content = article.content
        prompt = "Generate a 'brainrot' style narration for the following article:\n" + \
                f"\nTitle: {article_title}\n" + \
                f"\nContent: {article_content}\n" + \
                "Only output the narration in plain text, no other text."

        headers = get_json_headers()
        payload = {
            "model": self.model,
            "messages": [
                get_json_prompt(prompt)  # This returns {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"]
    
    def save_script(self, article_id: int, script: str) -> str:
        """
        Save generated script to temp folder.
        
        Args:
            article_id: ID of the article this script is based on
            script: Generated script text from generate_script()
        
        Returns:
            str: Path to the saved script file
        """
        script_path = os.path.join(settings.temp_dir, f"{article_id}.txt")
        with open(script_path, "w") as f:
            f.write(script)
        return script_path