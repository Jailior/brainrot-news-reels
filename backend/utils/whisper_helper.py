"""
Whisper transcription helper utilities.

This module provides functions for transcribing audio files using OpenAI Whisper
and extracting word-level timestamps. Used by AudioGenerator to create
caption data with precise timing information.

Interactions:
- Used by AudioGenerator.get_word_timestamps() to extract word timing
- Loads Whisper model and transcribes audio files
- Returns word-level timestamps for caption generation
- Requires whisper library to be installed
"""

import whisper
from typing import List, Dict, Optional
from pathlib import Path


class WhisperHelper:
    """
    Helper class for Whisper transcription operations.
    
    This class manages Whisper model loading and provides methods for
    transcribing audio with word-level timestamps.
    """
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper helper with model.
        
        Args:
            model_name: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                       Default 'base' provides good balance of speed and accuracy
        
        Note:
            Model is loaded lazily on first transcription to avoid loading
            large models at application startup.
        """
        self.model_name = model_name
        self._model: Optional[whisper.Whisper] = None
    
    def _load_model(self) -> whisper.Whisper:
        """
        Load Whisper model (lazy loading).
        
        Returns:
            whisper.Whisper: Loaded Whisper model instance
        
        Interactions:
            - Called automatically on first transcription
            - Model is cached in self._model for subsequent calls
        """
        if self._model is None:
            self._model = whisper.load_model(self.model_name)
        return self._model
    
    def transcribe_with_timestamps(self, audio_file_path: str) -> List[Dict]:
        """
        Transcribe audio file and extract word-level timestamps.
        
        Args:
            audio_file_path: Path to audio file (MP3, WAV, etc.)
        
        Returns:
            List[Dict]: List of word dictionaries with:
                - word: Word text
                - start: Start time in seconds (float)
                - end: End time in seconds (float)
        
        Raises:
            FileNotFoundError: If audio file doesn't exist
            RuntimeError: If transcription fails
        
        Interactions:
            - Called by AudioGenerator.get_word_timestamps()
            - Uses Whisper model to transcribe audio
            - Extracts word-level timing from transcription result
            - Returns data structure suitable for Caption model creation
        """
        # TODO: Implement Whisper transcription with word timestamps
        # Load model using _load_model()
        # Use model.transcribe() with word_timestamps=True
        # Parse result to extract word-level timing information
        # Return list of dictionaries with word, start, end keys
        # Handle errors appropriately
        pass
    
    def transcribe_simple(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to simple text (no timestamps).
        
        Useful for simple transcription needs without timing information.
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            str: Transcribed text
        
        Interactions:
            - Simpler alternative to transcribe_with_timestamps()
            - Returns plain text without timing information
        """
        # TODO: Implement simple transcription
        # Load model using _load_model()
        # Use model.transcribe() without word_timestamps
        # Extract text from result
        # Return transcribed text string
        pass

