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
from typing import Optional
from pathlib import Path
from urllib.parse import urlparse

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
        """
        self.bucket_name = settings.s3_bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    def _extract_s3_key(self, s3_key_or_url: str) -> str:
        """
        Accept either:
        - S3 key: "videos/reel_1.mp4"
        - S3 URL: "https://<bucket>.s3.<region>.amazonaws.com/videos/reel_1.mp4"
        - Path-style URL: "https://s3.<region>.amazonaws.com/<bucket>/videos/reel_1.mp4"
        - s3:// URL: "s3://<bucket>/videos/reel_1.mp4"

        And return: "videos/reel_1.mp4"
        """
        if not s3_key_or_url:
            raise ValueError("s3_key_or_url cannot be empty")

        s = s3_key_or_url.strip()

        # Already a key
        if "://" not in s:
            return s.lstrip("/")

        parsed = urlparse(s)

        # s3://bucket/key
        if parsed.scheme == "s3":
            return parsed.path.lstrip("/")

        # https://.../(bucket/)?key
        path = parsed.path.lstrip("/")
        if path.startswith(f"{self.bucket_name}/"):
            return path[len(self.bucket_name) + 1 :]
        return path

    
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
            str: S3 key of the uploaded file
        
        Raises:
            ClientError: If upload fails
        
        Interactions:
            - Called by AudioGenerator after generating audio file
            - Called by VideoCompositor after compositing final video
        """
        extra_args = {
            "ContentType": content_type or "application/octet-stream"
        }
        try:
            self.s3_client.upload_file(local_file_path, self.bucket_name, s3_key, ExtraArgs=extra_args)
            # Return a usable URL (handy for storing on Reel.video_url, etc.)
            return s3_key
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return None

    def download_file(self, s3_key_or_url: str, local_file_path: str) -> str:
        """
        Download a file from S3 to local filesystem.

        Args:
            s3_key_or_url: S3 object key OR a full S3 URL
            local_file_path: Local path where file should be saved

        Returns:
            str: local_file_path
        """
        s3_key = self._extract_s3_key(s3_key_or_url)
        Path(local_file_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_file_path)
            return local_file_path
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code")
            if code in {"404", "NoSuchKey", "NotFound"}:
                raise FileNotFoundError(f"S3 object not found: {s3_key}") from e
            raise
    
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
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")
            raise
    
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
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": s3_key},
            ExpiresIn=expires_in,
        )
    
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
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code")
            if code in {"404", "NoSuchKey", "NotFound"}:
                return False
            raise

