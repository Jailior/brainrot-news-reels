"""
Storage service for S3 file operations.

This service handles all interactions with S3 (or S3-compatible storage like
Cloudflare R2). It provides methods to upload, download, and delete files,
as well as generate presigned URLs for file access.

Interactions:
- Used by AudioGenerator to upload audio files to S3
- Used by VideoCompositor to download background videos and audio, upload final videos
- Uses config.py for S3 credentials and bucket configuration
- Uses boto3 library for AWS S3 operations
"""

import boto3
from botocore.exceptions import ClientError
from typing import Optional, BinaryIO
from pathlib import Path

from backend.config import settings


class StorageService:
    """
    Service for handling S3 file storage operations.
    
    This service abstracts S3 operations and can work with AWS S3 or
    S3-compatible services like Cloudflare R2 by configuring the endpoint URL.
    """
    
    def __init__(self):
        """
        Initialize the storage service with S3 client.
        
        Creates a boto3 S3 client using credentials from config.
        If S3_ENDPOINT_URL is set, uses it for S3-compatible services.
        """
        self.bucket_name = settings.s3_bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
            endpoint_url=settings.s3_endpoint_url,  # For Cloudflare R2 or other S3-compatible services
        )
    
    def upload_file(
        self,
        local_file_path: str,
        s3_key: str,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload a file from local filesystem to S3.
        
        Args:
            local_file_path: Path to the local file to upload
            s3_key: S3 object key (path within bucket)
            content_type: Optional MIME type (e.g., 'audio/mpeg', 'video/mp4')
        
        Returns:
            str: S3 URL of the uploaded file
        
        Raises:
            ClientError: If upload fails
        
        Interactions:
            - Called by AudioGenerator after generating audio file
            - Called by VideoCompositor after compositing final video
        """
        # TODO: Implement file upload to S3
        # Use self.s3_client.upload_file() with appropriate parameters
        # Return the S3 URL: f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{s3_key}"
        pass
    
    def download_file(self, s3_key: str, local_file_path: str) -> None:
        """
        Download a file from S3 to local filesystem.
        
        Args:
            s3_key: S3 object key (path within bucket)
            local_file_path: Local path where file should be saved
        
        Raises:
            ClientError: If download fails
            FileNotFoundError: If S3 key doesn't exist
        
        Interactions:
            - Called by VideoCompositor to download background videos and audio files
            - Downloads to /tmp directory for temporary processing
        """
        # TODO: Implement file download from S3
        # Use self.s3_client.download_file() with bucket_name and s3_key
        # Ensure parent directory exists before downloading
        pass
    
    def delete_file(self, s3_key: str) -> None:
        """
        Delete a file from S3.
        
        Args:
            s3_key: S3 object key to delete
        
        Raises:
            ClientError: If deletion fails
        
        Interactions:
            - Can be called for cleanup operations
            - Not typically used in main pipeline, but available for maintenance
        """
        # TODO: Implement file deletion from S3
        # Use self.s3_client.delete_object() with bucket_name and s3_key
        pass
    
    def get_file_url(self, s3_key: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for temporary file access.
        
        Args:
            s3_key: S3 object key
            expires_in: URL expiration time in seconds (default: 1 hour)
        
        Returns:
            str: Presigned URL that can be used to access the file
        
        Interactions:
            - Can be used to generate temporary access URLs for frontend
            - Alternative to public bucket URLs if bucket is private
        """
        # TODO: Implement presigned URL generation
        # Use self.s3_client.generate_presigned_url() with 'get_object' operation
        # Return the presigned URL string
        pass
    
    def file_exists(self, s3_key: str) -> bool:
        """
        Check if a file exists in S3.
        
        Args:
            s3_key: S3 object key to check
        
        Returns:
            bool: True if file exists, False otherwise
        
        Interactions:
            - Used for validation before operations
            - Can be used to avoid re-uploading existing files
        """
        # TODO: Implement file existence check
        # Use self.s3_client.head_object() and catch ClientError for 404
        # Return True if file exists, False if 404 error
        pass

