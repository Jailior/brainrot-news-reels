"""
Authentication routes for user login, signup, and profile management.
MVP implementation - no JWT, plain text password comparison.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.api.schemas.user import UserLogin, UserSignup, SetupRequest, UserResponse, UserUpdateRequest, DeleteAccountRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login", response_model=UserResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.
    Returns user data if credentials are valid.
    """
    logger.info(f"🔐 LOGIN ATTEMPT: email={credentials.email}")
    logger.info(f"📊 DB QUERY: SELECT * FROM users WHERE email='{credentials.email}'")
    
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        logger.warning(f"❌ LOGIN FAILED: User not found for email={credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Plain text password comparison (dev only)
    if user.hashed_password != credentials.password:
        logger.warning(f"❌ LOGIN FAILED: Invalid password for email={credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        logger.warning(f"❌ LOGIN FAILED: Account disabled for email={credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    logger.info(f"✅ LOGIN SUCCESS: user_id={user.id}, email={user.email}, name={user.name}")
    return user


@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    Create a new user account.
    Returns user data on success.
    """
    logger.info(f"📝 SIGNUP ATTEMPT: email={user_data.email}, name={user_data.name}")
    logger.info(f"📊 DB QUERY: SELECT * FROM users WHERE email='{user_data.email}'")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"❌ SIGNUP FAILED: Email already registered - {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (plain text password for dev)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=user_data.password,  # Plain text for MVP
        is_active=True,
        has_completed_setup=False
    )
    
    logger.info(f"📊 DB INSERT: INSERT INTO users (email, name, ...) VALUES ('{user_data.email}', '{user_data.name}', ...)")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"✅ SIGNUP SUCCESS: user_id={new_user.id}, email={new_user.email}")
    return new_user


@router.post("/setup", response_model=UserResponse)
async def update_setup(setup_data: SetupRequest, db: Session = Depends(get_db)):
    """
    Update user preferences and mark setup as complete.
    """
    logger.info(f"⚙️ SETUP UPDATE: user_id={setup_data.user_id}")
    logger.info(f"📊 DB QUERY: SELECT * FROM users WHERE id={setup_data.user_id}")
    
    user = db.query(User).filter(User.id == setup_data.user_id).first()
    
    if not user:
        logger.warning(f"❌ SETUP FAILED: User not found - user_id={setup_data.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"📊 DB UPDATE: UPDATE users SET preferences=..., has_completed_setup=true WHERE id={setup_data.user_id}")
    user.preferences = setup_data.preferences
    user.has_completed_setup = True
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"✅ SETUP SUCCESS: user_id={user.id}, preferences={setup_data.preferences}")
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Get user by ID.
    Used to fetch user data on app start.
    """
    logger.info(f"👤 GET USER: user_id={user_id}")
    logger.info(f"📊 DB QUERY: SELECT * FROM users WHERE id={user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        logger.warning(f"❌ GET USER FAILED: User not found - user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"✅ GET USER SUCCESS: user_id={user.id}, email={user.email}")
    return user


@router.put("/update-profile", response_model=UserResponse)
async def update_profile(update_data: UserUpdateRequest, db: Session = Depends(get_db)):
    """
    Update user profile (name and/or password).
    Requires current password if updating password.
    """
    logger.info(f"✏️ PROFILE UPDATE: user_id={update_data.user_id}")
    logger.info(f"📊 DB QUERY: SELECT * FROM users WHERE id={update_data.user_id}")
    
    user = db.query(User).filter(User.id == update_data.user_id).first()
    
    if not user:
        logger.warning(f"❌ PROFILE UPDATE FAILED: User not found - user_id={update_data.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # If updating password, verify current password
    if update_data.password:
        if not update_data.current_password:
            logger.warning(f"❌ PROFILE UPDATE FAILED: Current password required for password change")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required to change password"
            )
        
        # Verify current password matches
        if user.hashed_password != update_data.current_password:
            logger.warning(f"❌ PROFILE UPDATE FAILED: Invalid current password for user_id={update_data.user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        # Check that new password is different from current password
        if update_data.password == update_data.current_password:
            logger.warning(f"❌ PROFILE UPDATE FAILED: New password must be different from current password")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password"
            )
        
        logger.info(f"📊 DB UPDATE: UPDATE users SET hashed_password=... WHERE id={update_data.user_id}")
        user.hashed_password = update_data.password  # Plain text for MVP
    
    # Update name if provided
    if update_data.name is not None:
        logger.info(f"📊 DB UPDATE: UPDATE users SET name='{update_data.name}' WHERE id={update_data.user_id}")
        user.name = update_data.name
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"✅ PROFILE UPDATE SUCCESS: user_id={user.id}, name={user.name}")
    return user


@router.delete("/delete-account")
async def delete_account(delete_data: DeleteAccountRequest, db: Session = Depends(get_db)):
    """
    Delete user account.
    """
    logger.info(f"🗑️ DELETE ACCOUNT: user_id={delete_data.user_id}")
    logger.info(f"📊 DB QUERY: SELECT * FROM users WHERE id={delete_data.user_id}")
    
    user = db.query(User).filter(User.id == delete_data.user_id).first()
    
    if not user:
        logger.warning(f"❌ DELETE ACCOUNT FAILED: User not found - user_id={delete_data.user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"📊 DB DELETE: DELETE FROM users WHERE id={delete_data.user_id}")
    db.delete(user)
    db.commit()
    
    logger.info(f"✅ DELETE ACCOUNT SUCCESS: user_id={delete_data.user_id}")
    return {"message": "Account deleted successfully"}
