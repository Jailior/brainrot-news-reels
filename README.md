# Brainrot News Reels

Generate engaging "brainrot" style news reels automatically.

## Project Structure

### Frontend (Expo/React Native)
- `frontend/app/`: Expo Router routes.
  - `(auth)/`: Authentication screens (Login, Signup).
  - `(setup)/`: Onboarding questionnaire for user preferences.
  - `(tabs)/`: Main application tabs (Feed, Profile).
- `frontend/context/`: React Context providers (Auth).
- `frontend/hooks/`: Custom hooks for state management.
- `frontend/components/`: Reusable UI components.

### Backend (FastAPI/Python)
- `backend/api/routes/`: API endpoints.
  - `auth.py`: User authentication and setup.
  - `reels.py`: Reel management and retrieval.
  - `generate.py`: Content generation triggers.
- `backend/models/`: SQLAlchemy database models.
- `backend/services/`: Business logic and external integrations (OpenAI, AWS S3, etc.).
- `backend/database.py`: Database connection and session management.

## Getting Started

### Prerequisites
- Node.js & npm
- Python 3.10+
- PostgreSQL (or SQLite for local development)

### Setup

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn backend.main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npx expo start
   ```
