"""
Services package.

This package contains all business logic services for the application.
Services handle external API integrations, file processing, and orchestrate
the reel generation pipeline.

Services:
- NewsFetcher: Fetches articles from NewsAPI
- ScriptGenerator: Generates scripts using Claude API
- AudioGenerator: Generates audio using ElevenLabs API
- VideoCompositor: Composites videos using FFmpeg
- StorageService: Handles S3 file operations
"""

from backend.services.news_fetcher import NewsFetcher
from backend.services.script_generator import ScriptGenerator
from backend.services.audio_generator import AudioGenerator
from backend.services.video_compositor import VideoCompositor
from backend.services.storage_service import StorageService

__all__ = [
    "NewsFetcher",
    "ScriptGenerator",
    "AudioGenerator",
    "VideoCompositor",
    "StorageService",
]

