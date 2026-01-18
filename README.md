# Brainrot News Reels

Generate engaging "brainrot" style news reels automatically.

## Prerequisites

- Node.js & npm
- Python 3.10+
- PostgreSQL 16+

## Quick Start

### 1. PostgreSQL Setup

Run the setup script for your platform:

```bash
# macOS
./scripts/setup_postgres_macos.sh

# Linux
sudo ./scripts/setup_postgres_linux.sh

# Windows (PowerShell)
.\scripts\setup_postgres_windows.ps1
```

Or follow the detailed guide in [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md).

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
DB_USER=dev_user
DB_PASSWORD=dev_pw
DB_HOST=localhost
DB_PORT=5432
DB_NAME=brainrot_news_reels
```

### 3. Backend

```bash
cd backend
pip install -e .
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at `http://localhost:8000`. Database tables are created automatically on startup.

### 4. Frontend

```bash
cd frontend
npm install
npx expo start
```

Press `i` for iOS, `a` for Android, `w` for web, or scan QR code with Expo Go.

## Project Structure

- **Frontend**: Expo/React Native app in `frontend/`
- **Backend**: FastAPI application in `backend/`
- **Database**: PostgreSQL (auto-initialized on backend startup)
