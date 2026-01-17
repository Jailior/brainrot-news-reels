"""
Audio generator service for ElevenLabs API integration.

This service generates audio from scripts using ElevenLabs text-to-speech API,
saves the audio file temporarily, uploads it to S3, extracts word-level timestamps
using Whisper, and saves captions to the database.

Interactions:
- Reads script from Reel (via ScriptGenerator.get_script_by_reel_id)
- Calls ElevenLabs API to generate audio
- Saves MP3 to /tmp directory temporarily
- Uses StorageService to upload audio to S3
- Uses WhisperHelper to extract word timestamps
- Saves captions to database using Caption model
- Updates Reel.audio_url and Reel.status
"""

import requests
import os
from pathlib import Path
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.reel import Reel, ReelStatus
from backend.models.caption import Caption
from backend.services.storage_service import StorageService
from backend.utils.whisper_helper import WhisperHelper


class AudioGenerator:
    """
    Service for generating audio from scripts using ElevenLabs API.
    
    This service handles the complete audio generation pipeline:
    1. Generate audio via ElevenLabs API
    2. Save to temporary file
    3. Upload to S3
    4. Extract word timestamps with Whisper
    5. Save captions to database
    """
    
    def __init__(self):
        """
        Initialize the audio generator with API configuration.
        
        Uses settings from config.py for API key, base URL, and voice ID.
        Initializes StorageService for S3 operations.
        Initializes WhisperHelper for transcription.
        """
        self.api_key = settings.elevenlabs_api_key
        self.base_url = settings.elevenlabs_base_url
        self.voice_id = settings.elevenlabs_voice_id
        self.temp_dir = settings.temp_dir
        self.storage_service = StorageService()
        self.whisper_helper = WhisperHelper()
    
    def generate_audio(self, script: str, output_path: str) -> None:
        """
        Generate audio file from script text using ElevenLabs API.
        
        Args:
            script: Script text to convert to speech
            output_path: Local file path where MP3 should be saved
        
        Raises:
            requests.RequestException: If API call fails
            ValueError: If API key is not configured
            IOError: If file cannot be written
        
        Interactions:
            - Called with script text from Reel
            - Saves MP3 file to output_path (typically /tmp directory)
            - File will be uploaded to S3 after generation
        """
        # TODO: Implement ElevenLabs API call
        # Use requests.post() to call ElevenLabs text-to-speech endpoint
        # Include script text and voice_id in request
        # Stream response and save to output_path as MP3
        # Ensure output directory exists before writing
        pass
    
    def save_audio_to_temp(self, script: str, reel_id: int) -> str:
        """
        Generate audio and save to temporary directory.
        
        Args:
            script: Script text to convert to speech
            reel_id: ID of the reel (for filename)
        
        Returns:
            str: Path to the temporary audio file
        
        Interactions:
            - Calls generate_audio() to create MP3
            - Saves to /tmp directory with unique filename
            - Returns path for upload_audio_to_s3()
        """
        # TODO: Implement temporary file saving
        # Create unique filename: f"audio_{reel_id}_{timestamp}.mp3"
        # Construct full path in temp_dir
        # Call generate_audio() with script and output path
        # Return the file path
        pass
    
    def upload_audio_to_s3(self, local_file_path: str, reel_id: int) -> str:
        """
        Upload audio file from temporary location to S3.
        
        Args:
            local_file_path: Path to local MP3 file
            reel_id: ID of the reel (for S3 key)
        
        Returns:
            str: S3 URL of the uploaded audio file
        
        Interactions:
            - Uses StorageService.upload_file() to upload to S3
            - S3 key format: "audio/reel_{reel_id}.mp3"
            - Returns URL to be saved in Reel.audio_url
        """
        # TODO: Implement S3 upload
        # Construct S3 key: f"audio/reel_{reel_id}.mp3"
        # Use self.storage_service.upload_file() with content_type='audio/mpeg'
        # Return the S3 URL
        pass
    
    def get_word_timestamps(self, audio_file_path: str) -> List[Dict]:
        """
        Extract word-level timestamps from audio using Whisper.
        
        Args:
            audio_file_path: Path to audio file (local or S3 URL)
        
        Returns:
            List[Dict]: List of word dictionaries with:
                - word: Word text
                - start: Start time in seconds
                - end: End time in seconds
        
        Interactions:
            - Uses WhisperHelper to transcribe audio with word timestamps
            - Returns data that will be saved as Caption records
        """
        # TODO: Implement Whisper transcription
        # If audio_file_path is S3 URL, download to temp first
        # Use self.whisper_helper.transcribe_with_timestamps()
        # Return list of word dictionaries with timing information
        pass
    
    def save_captions(self, reel_id: int, word_timestamps: List[Dict], db: Session) -> List[Caption]:
        """
        Save word timestamps as Caption records in database.
        
        Args:
            reel_id: ID of the reel these captions belong to
            word_timestamps: List of word dictionaries from get_word_timestamps()
            db: Database session
        
        Returns:
            List[Caption]: List of created Caption model instances
        
        Interactions:
            - Creates Caption records linked to Reel
            - Sets sequence_order based on timestamp order
            - Used by VideoCompositor to generate SRT subtitle files
        """
        # TODO: Implement caption saving
        # Create Caption instances from word_timestamps
        # Set sequence_order based on start_time
        # Use db.add_all() and db.commit() to save
        # Return list of created Caption objects
        pass
    
    def process_reel_audio(self, reel_id: int, db: Session) -> Reel:
        """
        Complete audio generation pipeline for a reel.
        
        This method orchestrates the full audio generation process:
        1. Get script from database
        2. Generate audio and save to temp
        3. Upload to S3
        4. Extract word timestamps
        5. Save captions
        6. Update reel status and audio_url
        
        Args:
            reel_id: ID of the reel to process
            db: Database session
        
        Returns:
            Reel: Updated Reel instance with audio_url set
        
        Interactions:
            - Orchestrates all audio generation steps
            - Updates Reel.status to AUDIO_GENERATED
            - Updates Reel.audio_url with S3 URL
        """
        # TODO: Implement full audio pipeline
        # Get Reel from database
        # Get script text from Reel.script
        # Call save_audio_to_temp() to generate and save audio
        # Call upload_audio_to_s3() to upload
        # Call get_word_timestamps() to extract timing
        # Call save_captions() to persist captions
        # Update Reel.audio_url and Reel.status = ReelStatus.AUDIO_GENERATED
        # Commit changes and return updated Reel
        pass

