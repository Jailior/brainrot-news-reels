"""
Video compositor service for FFmpeg video composition.

This service handles the complete video composition pipeline:
1. Get random background video from database
2. Download background video and audio from S3
3. Generate SRT subtitle file from captions
4. Use FFmpeg to composite video (background + audio + captions)
5. Upload final video to S3
6. Update reel status to 'ready'

Interactions:
- Reads BackgroundVideo from database for random selection
- Uses StorageService to download/upload files
- Reads Caption records from database to generate SRT
- Uses FFmpeg via subprocess to composite video
- Updates Reel.video_url and Reel.status to READY
"""

import subprocess
import random
import os
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.reel import Reel, ReelStatus
from backend.models.background_video import BackgroundVideo
from backend.models.caption import Caption
from backend.services.storage_service import StorageService


class VideoCompositor:
    """
    Service for compositing final videos using FFmpeg.
    
    This service handles the complete video composition pipeline:
    1. Background video (from S3)
    2. Audio overlay (from S3)
    3. Caption burn-in (from SRT file)
    4. Final video upload to S3
    """
    
    def __init__(self):
        """
        Initialize the video compositor.
        
        Uses settings from config.py for temp directory.
        Initializes StorageService for S3 operations.
        """
        self.temp_dir = settings.temp_dir
        self.storage_service = StorageService()
    

    def get_random_background_video(self, db: Session) -> Optional[BackgroundVideo]:
        """
        Retrieve a random background video from the database.
        
        Args:
            db: Database session
        
        Returns:
            Optional[BackgroundVideo]: Random BackgroundVideo instance, None if none exist
        
        Interactions:
            - Queries background_videos table
            - Returns random selection for video composition
            - BackgroundVideo.s3_url is used to download the video file
        """
        # TODO: Implement random background video selection
        # Query all BackgroundVideo records from database
        # Use random.choice() to select one
        # Return BackgroundVideo instance or None if empty
        pass
    

    def download_from_s3(self, s3_url: str, local_file_path: str) -> None:
        """
        Download a file from S3 to local filesystem.
        
        Args:
            s3_url: Full S3 URL of the file
            local_file_path: Local path where file should be saved
        
        Raises:
            ValueError: If S3 URL is invalid
            IOError: If download fails
        
        Interactions:
            - Uses StorageService to download files
            - Extracts S3 key from URL before calling storage service
            - Downloads background videos and audio files to /tmp for processing
        """
        # TODO: Implement S3 download
        # Parse S3 key from s3_url (extract path after bucket name)
        # Use self.storage_service.download_file() to download
        # Ensure parent directory exists before downloading
        self.storage_service.download_file(s3_url, local_file_path)

    
    def generate_srt_file(self, captions: list[dict], output_path: str) -> None:
        """
        Generate SRT subtitle file from caption records.
        
        Args:
            captions: List of Caption dictionaries (ordered by sequence_order)
            output_path: Path where SRT file should be saved
        
        Raises:
            IOError: If file cannot be written
        
        Interactions:
            - Reads Caption records from database (ordered by sequence_order)
            - Generates standard SRT format with timestamps
            - SRT file is used by FFmpeg to burn captions into video
        """
        def format_time(time: float) -> str:
            hours = int(time // 3600)
            minutes = int((time % 3600) // 60)
            seconds = int(time % 60)
            milliseconds = int((time * 1000) % 1000)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

        # Write as UTF-8 so FFmpeg can decode “smart quotes”, em-dashes, etc.
        # (Windows default encodings like cp1252 will trigger "Invalid UTF-8" and
        # can cause subtitles to stop rendering after the first few cues.)
        with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
            for seq_order,caption in enumerate(captions):
                f.write(f"{seq_order + 1}\n{format_time(caption['start_time'])} --> {format_time(caption['end_time'])}\n{caption['text']}\n\n")
    
    def composite_video(
        self,
        background_video_path: str,
        audio_path: str,
        srt_path: str,
        output_video_path: str,
    ) -> None:
        """
        Composite final video using FFmpeg.
        
        Combines background video, audio, and captions into final video.
        Uses FFmpeg -shortest flag to automatically trim background video
        to match audio length.
        
        Args:
            background_video_path: Path to background video file
            audio_path: Path to audio file
            srt_path: Path to SRT subtitle file
            output_video_path: Path where final video should be saved
        
        Raises:
            subprocess.CalledProcessError: If FFmpeg command fails
            FileNotFoundError: If FFmpeg is not installed
        
        Interactions:
            - Runs FFmpeg subprocess to composite video
            - Uses -shortest flag to trim background to audio length
            - Burns captions into video using subtitles filter
            - Output video is uploaded to S3 after composition
        """
        # TODO: Implement FFmpeg video composition
        # FFmpeg command structure:
        # ffmpeg -i background.mp4 -i audio.mp3 -vf subtitles=subtitles.srt
        #        -shortest -c:v libx264 -c:a aac output.mp4
        # Use subprocess.run() to execute FFmpeg
        # -shortest flag automatically trims to audio length
        # Handle errors and validate input files exist
        style="Fontname=Impact,Fontsize=14,PrimaryColour=&H00FF4000,OutlineColour=&H000000,Outline=1,Alignment=10"
        subprocess.run([
            'ffmpeg',
            '-y',
            '-i', background_video_path,
            '-i', audio_path,
            '-vf', f"scale=iw*3:ih*3,subtitles={srt_path}:force_style='{style}'",
            # Ensure we use background video + narration audio (not background audio)
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            output_video_path
        ], check=True)
    

    def upload_video_to_s3(self, local_file_path: str, reel_id: int) -> str:
        """
        Upload final video file to S3.
        
        Args:
            local_file_path: Path to local video file
            reel_id: ID of the reel (for S3 key)
        
        Returns:
            str: S3 URL of the uploaded video file
        
        Interactions:
            - Uses StorageService to upload video
            - S3 key format: "videos/reel_{reel_id}.mp4"
            - Returns URL to be saved in Reel.video_url
        """
        return self.storage_service.upload_file(
            local_file_path, 
            f"videos/reel_{reel_id}.mp4", 
            content_type='video/mp4'
        )
    
    def update_reel_status(self, reel_id: int, video_url: str, db: Session) -> Reel:
        """
        Update reel with video URL and mark as ready.
        
        Args:
            reel_id: ID of the reel to update
            video_url: S3 URL of the final video
            db: Database session
        
        Returns:
            Reel: Updated Reel instance
        
        Interactions:
            - Updates Reel.video_url with S3 URL
            - Sets Reel.status to READY
            - Reel is now available for frontend consumption
        """
        # TODO: Implement reel status update
        # Get Reel from database by ID
        # Set Reel.video_url = video_url
        # Set Reel.status = ReelStatus.READY
        # Commit changes and return updated Reel
        pass
    
    def process_reel_video(self, reel_id: int, db: Session) -> Reel:
        """
        Complete video composition pipeline for a reel.
        
        This method orchestrates the full video composition process:
        1. Get random background video
        2. Download background video and audio from S3
        3. Get captions from database
        4. Generate SRT file
        5. Composite video with FFmpeg
        6. Upload final video to S3
        7. Update reel status to ready
        
        Args:
            reel_id: ID of the reel to process
            db: Database session
        
        Returns:
            Reel: Updated Reel instance with video_url set and status=READY
        
        Interactions:
            - Orchestrates all video composition steps
            - Cleans up temporary files after processing
            - Updates Reel with final video URL and ready status
        """
        # TODO: Implement full video composition pipeline
        # Get Reel from database
        # Get random background video using get_random_background_video()
        # Download background video to /tmp
        # Download audio from Reel.audio_url to /tmp
        # Get captions from database (Reel.captions)
        # Generate SRT file using generate_srt_file()
        # Composite video using composite_video()
        # Upload video using upload_video_to_s3()
        # Update reel status using update_reel_status()
        # Clean up temporary files
        # Return updated Reel
        pass

