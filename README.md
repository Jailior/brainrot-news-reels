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
- PostgreSQL (see [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for installation instructions)

### Setup

1. **PostgreSQL Database**:
   - Follow the comprehensive guide in [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)
   - Or use the automated setup scripts in `scripts/` directory:
     - macOS: `./scripts/setup_postgres_macos.sh`
     - Linux: `sudo ./scripts/setup_postgres_linux.sh`
     - Windows: `.\scripts\setup_postgres_windows.ps1` (PowerShell) or `.\scripts\setup_postgres_windows.bat` (CMD)

2. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   # Ensure .env file is configured (see POSTGRESQL_SETUP.md)
   uvicorn backend.main:app --reload
   ```

3. **Frontend**:
   ```bash
   cd frontend
   npm install
   npx expo start
   ```
