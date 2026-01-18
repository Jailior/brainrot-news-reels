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
from backend.models.reel_watch import ReelWatch
from backend.models.user import User
from backend.api.schemas.reel import (
    ReelResponse,
    ReelListResponse,
    ReelDetailResponse,
    ViewIncrementResponse,
    UserWatchedReelsResponse,
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
    user_id: int = Query(None, description="Optional user ID to track watch history"),
    db: Session = Depends(get_db),
) -> ViewIncrementResponse:
    """
    Increment the view count for a reel.
    
    Called by frontend when a user views a reel. Updates the views counter
    in the database. Optionally tracks watch history if user_id is provided.
    
    Args:
        reel_id: ID of the reel to increment views for
        user_id: Optional user ID to record watch history
        db: Database session (injected)
    
    Returns:
        ViewIncrementResponse: Updated view count
    
    Raises:
        HTTPException: 404 if reel not found or user not found (if user_id provided)
    
    Interactions:
        - Gets Reel by ID from database
        - If user_id provided, validates user exists and creates/updates ReelWatch record
        - Increments Reel.views by 1
        - Commits changes to database
        - Returns updated view count
    """
    # Query Reel by ID
    reel = db.query(Reel).filter(Reel.id == reel_id).first()
    if not reel:
        raise HTTPException(status_code=404, detail="Reel not found")
    
    # If user_id is provided, track watch history
    if user_id is not None:
        # Validate user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create or get existing watch record (unique constraint prevents duplicates)
        watch_record = db.query(ReelWatch).filter(
            ReelWatch.user_id == user_id,
            ReelWatch.reel_id == reel_id
        ).first()
        
        if not watch_record:
            watch_record = ReelWatch(user_id=user_id, reel_id=reel_id)
            db.add(watch_record)
    
    # Increment view count
    reel.views += 1
    db.commit()
    db.refresh(reel)
    
    return ViewIncrementResponse(reel_id=reel.id, views=reel.views)


@router.get("/reels/users/{user_id}/watched", response_model=UserWatchedReelsResponse)
def get_user_watched_reels(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserWatchedReelsResponse:
    """
    Get all reels that a user has watched.
    
    Returns a list of all reels the user has watched, based on watch history records.
    
    Args:
        user_id: ID of the user to get watched reels for
        db: Database session (injected)
    
    Returns:
        UserWatchedReelsResponse: List of reels the user has watched
    
    Raises:
        HTTPException: 404 if user not found
    
    Interactions:
        - Validates user exists
        - Queries ReelWatch table filtered by user_id
        - Joins with Reel table to get full reel details
        - Returns list of ReelResponse objects
    """
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Query watch history for this user
    watch_records = db.query(ReelWatch).filter(ReelWatch.user_id == user_id).all()
    
    # Get all reels that the user has watched
    reel_ids = [watch.reel_id for watch in watch_records]
    reels = db.query(Reel).filter(Reel.id.in_(reel_ids)).all() if reel_ids else []
    
    # Convert to ReelResponse objects
    reel_responses = [
        ReelResponse(
            id=reel.id,
            video_url=reel.video_url,
            script=reel.script,
            views=reel.views,
            created_at=reel.created_at,
        )
        for reel in reels
    ]
    
    return UserWatchedReelsResponse(reels=reel_responses)

