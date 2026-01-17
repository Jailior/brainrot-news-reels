"""
Reel API routes.

This module contains FastAPI route handlers for reel-related endpoints.
Handles fetching reels, getting reel details, and incrementing view counts.

Interactions:
- Uses Reel model from database
- Uses ReelResponse, ReelListResponse schemas for responses
- Uses database session via dependency injection
- Called by frontend to fetch and display reels
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.reel import Reel, ReelStatus
from backend.api.schemas.reel import (
    ReelResponse,
    ReelListResponse,
    ReelDetailResponse,
    ViewIncrementResponse,
)

router = APIRouter()


@router.get("/reels", response_model=ReelListResponse)
def get_reels(
    limit: int = Query(default=10, ge=1, le=100, description="Number of reels to return"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
) -> ReelListResponse:
    """
    Get paginated list of ready reels.
    
    Returns only reels with status='ready' that have video_url set.
    Used by frontend for infinite scroll functionality.
    
    Args:
        limit: Maximum number of reels to return (1-100)
        offset: Number of reels to skip for pagination
        db: Database session (injected)
    
    Returns:
        ReelListResponse: Paginated list of ready reels with metadata
    
    Interactions:
        - Queries Reel table filtered by status=READY
        - Orders by created_at descending (newest first)
        - Returns ReelListResponse with reels, total count, limit, offset
        - Frontend uses this for initial load and infinite scroll
    """
    # TODO: Implement reel listing
    # Query reels with status=ReelStatus.READY and video_url is not None
    # Order by created_at descending
    # Apply limit and offset for pagination
    # Count total number of ready reels
    # Convert to ReelResponse objects
    # Return ReelListResponse with reels list, total, limit, offset
    pass


@router.get("/reels/{reel_id}", response_model=ReelDetailResponse)
def get_reel_detail(
    reel_id: int,
    db: Session = Depends(get_db),
) -> ReelDetailResponse:
    """
    Get detailed information about a specific reel.
    
    Returns extended reel information including article title and audio URL.
    
    Args:
        reel_id: ID of the reel to retrieve
        db: Database session (injected)
    
    Returns:
        ReelDetailResponse: Detailed reel information
    
    Raises:
        HTTPException: 404 if reel not found
    
    Interactions:
        - Queries Reel by ID
        - Includes related Article information
        - Returns ReelDetailResponse with all reel details
    """
    # TODO: Implement reel detail retrieval
    # Query Reel by ID, include article relationship
    # If not found, raise HTTPException(status_code=404)
    # Convert to ReelDetailResponse including article_title
    # Return ReelDetailResponse
    pass


@router.post("/reels/{reel_id}/view", response_model=ViewIncrementResponse)
def increment_view_count(
    reel_id: int,
    db: Session = Depends(get_db),
) -> ViewIncrementResponse:
    """
    Increment the view count for a reel.
    
    Called by frontend when a user views a reel. Updates the views counter
    in the database.
    
    Args:
        reel_id: ID of the reel to increment views for
        db: Database session (injected)
    
    Returns:
        ViewIncrementResponse: Updated view count
    
    Raises:
        HTTPException: 404 if reel not found
    
    Interactions:
        - Gets Reel by ID from database
        - Increments Reel.views by 1
        - Commits changes to database
        - Returns updated view count
    """
    # TODO: Implement view count increment
    # Query Reel by ID
    # If not found, raise HTTPException(status_code=404)
    # Increment Reel.views by 1
    # Commit changes
    # Return ViewIncrementResponse with reel_id and updated views
    pass

