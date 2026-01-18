"""
Audio generator service for ElevenLabs API integration.

This service generates audio from scripts using ElevenLabs text-to-speech API,
saves the audio file temporarily, extracts word-level timestamps, and returns the timestamps.

Interactions:
- Calls ElevenLabs API to generate audio
- Extracts word timestamps from audio
- Saves MP3 to temporary directory
"""

import base64
import os

from backend.config import settings
from elevenlabs.client import ElevenLabs 


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
        self.client = ElevenLabs(api_key=self.api_key)
        self.temp_dir = settings.temp_dir

    
    def generate_audio(self, script: str, output_path: str, voice_id: str):
        """
        Generate audio file from script text using ElevenLabs API and returns response object.
        
        Args:
            script: Script text to convert to speech
            output_path: Local file path where MP3 should be saved
            voice_id: ElevenLabs voice ID to use for audio generation
        
        Returns:
            AudioWithTimestampsResponse:
                - audio_base_64: base64 encoded audio
                - alignments: list of alignments
        """
        try:
            response = self.client.text_to_speech.convert_with_timestamps(
                text=script,
                voice_id=voice_id,
            )
        except Exception as e:
            print("Error generating audio from ElevenLabs API: ", e)
            return None
        return response
    

    def get_word_timestamps(self, alignments, max_chars):
        """
        Groups words based on MAX_CHAR_TO_DISPLAY and maps groups to starting word timestamps.
        
        Args:
            alignments (dict): The alignment data from ElevenLabs API response containing:
                - characters: list of individual characters
                - character_start_times_seconds: list of start times for each character
                - character_end_times_seconds: list of end times for each character
            script (str): The original script text used to generate the audio
            max_chars (int): Maximum characters to display per group (from settings.MAX_CHAR_TO_DISPLAY)
        
        Returns:
            list: List of dictionaries with structure:
                [
                    {
                        'text': 'grouped words',
                        'start_time': float (seconds),
                        'end_time': float (seconds)
                    },
                    ...
                ]
        """
        if not alignments:
            return []
        
        characters = alignments.characters
        start_times = alignments.character_start_times_seconds
        end_times = alignments.character_end_times_seconds
        
        # Reconstruct words from characters
        words = []
        current_word = []
        word_start_idx = 0
        
        for i, char in enumerate(characters):
            if char.isspace() or char in '.,!?;:—-':
                if current_word:
                    words.append({
                        'text': ''.join(current_word),
                        'start_idx': word_start_idx,
                        'end_idx': i - 1,
                        'start_time': start_times[word_start_idx],
                        'end_time': end_times[i - 1]
                    })
                    current_word = []
                # Include space/punctuation in the previous word's end time
                if words and i < len(end_times):
                    words[-1]['end_time'] = end_times[i]
                    words[-1]['text'] += char
            else:
                if not current_word:
                    word_start_idx = i
                current_word.append(char)
        
        # Add the last word if exists
        if current_word:
            words.append({
                'text': ''.join(current_word),
                'start_idx': word_start_idx,
                'end_idx': len(characters) - 1,
                'start_time': start_times[word_start_idx],
                'end_time': end_times[len(characters) - 1]
            })
        
        # Group words by character limit
        groups = []
        current_group = []
        current_length = 0
        
        for word in words:
            word_text = word['text']
            word_length = len(word_text)
            
            # Check if adding this word would exceed the limit
            if current_group and (current_length + word_length > max_chars):
                # Finalize current group
                group_text = ''.join([w['text'] for w in current_group])
                groups.append({
                    'text': group_text.strip(),
                    'start_time': current_group[0]['start_time'],
                    'end_time': current_group[-1]['end_time']
                })
                # Start new group
                current_group = [word]
                current_length = word_length
            else:
                # Add word to current group
                current_group.append(word)
                current_length += word_length
        
        # Add the last group
        if current_group:
            group_text = ''.join([w['text'] for w in current_group])
            groups.append({
                'text': group_text.strip(),
                'start_time': current_group[0]['start_time'],
                'end_time': current_group[-1]['end_time']
            })
        
        return groups

    
    def save_audio_to_temp(self, response, temp_id_name: str) -> str:
        """
        Save audio file from response object to temporary directory.
        
        Args:
            response: response object from generate_audio()
            temp_id_name: Name of the temporary file
        
        Returns:
            str: Path to the temporary audio file
        """
        audio_base64 = response.audio_base_64
        audio_path = os.path.join(self.temp_dir, f"{temp_id_name}.mp3")
        with open(audio_path, "wb") as f:
            f.write(base64.b64decode(audio_base64))
        return audio_path
