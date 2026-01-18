#!/usr/bin/env python3
"""
Script to create a guest user for development testing.
Run this script once to populate the database with a guest user.

Usage:
    cd /path/to/brainrot-news-reels
    source venv/bin/activate
    python scripts/create_guest_user.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, init_db
from backend.models.user import User


def create_guest_user():
    """Create a guest user if it doesn't exist."""
    
    # Initialize database tables
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if guest user already exists
        existing_guest = db.query(User).filter(User.email == "guest@brainrot.app").first()
        
        if existing_guest:
            print("Guest user already exists:")
            print(f"  ID: {existing_guest.id}")
            print(f"  Email: {existing_guest.email}")
            print(f"  Name: {existing_guest.name}")
            return existing_guest
        
        # Create guest user
        guest_user = User(
            email="guest@brainrot.app",
            name="guest",
            hashed_password="guest123",  # Plain text for dev
            is_active=True,
            has_completed_setup=True,
            preferences={
                "categories": ["Technology", "Science"],
                "language": "English"
            }
        )
        
        db.add(guest_user)
        db.commit()
        db.refresh(guest_user)
        
        print("Guest user created successfully!")
        print(f"  ID: {guest_user.id}")
        print(f"  Email: {guest_user.email}")
        print(f"  Name: {guest_user.name}")
        print(f"  Password: guest123")
        
        return guest_user
        
    except Exception as e:
        print(f"Error creating guest user: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_guest_user()
