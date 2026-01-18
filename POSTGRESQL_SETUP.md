# PostgreSQL Setup Guide

This guide will walk you through setting up PostgreSQL from scratch for the Brainrot News Reels project on macOS, Windows, and Linux.

## Table of Contents

- [macOS Setup](#macos-setup)
- [Windows Setup](#windows-setup)
- [Linux Setup](#linux-setup)
- [Database Configuration](#database-configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## macOS Setup

### Prerequisites

- macOS 10.15 or later
- Homebrew (if not installed, see below)

### Step 1: Install Homebrew (if needed)

If you don't have Homebrew installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify installation:
```bash
brew --version
```

### Step 2: Install PostgreSQL

```bash
brew install postgresql@16
```

### Step 3: Start PostgreSQL Service

```bash
brew services start postgresql@16
```

### Step 4: Add PostgreSQL to PATH

Add PostgreSQL to your shell configuration:

**For zsh (default on macOS Catalina+):**
```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

**Note:** On Intel Macs, the path might be `/usr/local/opt/postgresql@16/bin` instead of `/opt/homebrew/opt/postgresql@16/bin`.

### Step 5: Verify Installation

```bash
psql --version
```

You should see something like: `psql (PostgreSQL) 16.x`

### Step 6: Create Database and User

Run the setup script or manually execute:

```bash
# Connect to PostgreSQL (default superuser is your macOS username)
psql postgres

# In the psql prompt, run:
CREATE DATABASE brainrot_news_reels;
CREATE USER dev_user WITH PASSWORD 'dev_pw';
GRANT ALL PRIVILEGES ON DATABASE brainrot_news_reels TO dev_user;
\c brainrot_news_reels
GRANT ALL ON SCHEMA public TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO dev_user;
\q
```

**Or use the automated script:**
```bash
chmod +x scripts/setup_postgres_macos.sh
./scripts/setup_postgres_macos.sh
```

---

## Windows Setup

### Prerequisites

- Windows 10 or later
- Administrator privileges

### Step 1: Download PostgreSQL

1. Visit [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)
2. Download the installer from EnterpriseDB (recommended)
3. Run the installer executable

### Step 2: Install PostgreSQL

1. **Welcome Screen**: Click "Next"
2. **Installation Directory**: Use default or choose custom location, click "Next"
3. **Select Components**: Ensure all components are selected, click "Next"
4. **Data Directory**: Use default location, click "Next"
5. **Password**: 
   - Set a password for the `postgres` superuser account
   - **IMPORTANT**: Remember this password! You'll need it later.
   - Click "Next"
6. **Port**: Keep default port `5432`, click "Next"
7. **Advanced Options**: Use default locale, click "Next"
8. **Pre Installation Summary**: Review and click "Next"
9. **Ready to Install**: Click "Next" to begin installation
10. **Completing Installation**: 
    - Uncheck "Launch Stack Builder" (optional)
    - Click "Finish"

### Step 3: Add PostgreSQL to PATH

1. Open **System Properties** → **Environment Variables**
2. Under **System Variables**, find and select `Path`, click **Edit**
3. Click **New** and add:
   ```
   C:\Program Files\PostgreSQL\16\bin
   ```
   (Adjust version number if different)
4. Click **OK** on all dialogs

**Alternative (PowerShell as Administrator):**
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\16\bin", "Machine")
```

### Step 4: Verify Installation

Open a **new** Command Prompt or PowerShell window:

```cmd
psql --version
```

You should see: `psql (PostgreSQL) 16.x`

### Step 5: Start PostgreSQL Service

PostgreSQL should start automatically, but if needed:

**Using Services:**
1. Press `Win + R`, type `services.msc`, press Enter
2. Find "postgresql-x64-16" (or similar)
3. Right-click → **Start** (if not running)

**Using Command Prompt (as Administrator):**
```cmd
net start postgresql-x64-16
```

### Step 6: Create Database and User

**Using Command Prompt or PowerShell:**

```cmd
psql -U postgres
```

You'll be prompted for the password you set during installation.

In the psql prompt:
```sql
CREATE DATABASE brainrot_news_reels;
CREATE USER dev_user WITH PASSWORD 'dev_pw';
GRANT ALL PRIVILEGES ON DATABASE brainrot_news_reels TO dev_user;
\c brainrot_news_reels
GRANT ALL ON SCHEMA public TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO dev_user;
\q
```

**Or use the automated PowerShell script:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\scripts\setup_postgres_windows.ps1
```

**Or use the batch script:**
```cmd
scripts\setup_postgres_windows.bat
```

---

## Linux Setup

### Prerequisites

- Ubuntu/Debian, Fedora, or other Linux distribution
- sudo privileges

### Ubuntu/Debian

#### Step 1: Update Package List

```bash
sudo apt update
```

#### Step 2: Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib
```

#### Step 3: Start PostgreSQL Service

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql  # Enable auto-start on boot
```

#### Step 4: Verify Installation

```bash
psql --version
sudo systemctl status postgresql
```

### Fedora/RHEL/CentOS

#### Step 1: Install PostgreSQL

```bash
sudo dnf install postgresql-server postgresql
```

#### Step 2: Initialize Database

```bash
sudo postgresql-setup --initdb
```

#### Step 3: Start PostgreSQL Service

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Step 4: Verify Installation

```bash
psql --version
sudo systemctl status postgresql
```

### Step 5: Create Database and User (All Linux Distributions)

Switch to the postgres user and create the database:

```bash
sudo -u postgres psql
```

In the psql prompt:
```sql
CREATE DATABASE brainrot_news_reels;
CREATE USER dev_user WITH PASSWORD 'dev_pw';
GRANT ALL PRIVILEGES ON DATABASE brainrot_news_reels TO dev_user;
\c brainrot_news_reels
GRANT ALL ON SCHEMA public TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO dev_user;
\q
```

**Or use the automated script:**
```bash
chmod +x scripts/setup_postgres_linux.sh
sudo ./scripts/setup_postgres_linux.sh
```

---

## Database Configuration

### Step 1: Create .env File

Create a `.env` file in the project root with the following content:

```env
# Database Configuration
DB_USER=dev_user
DB_PASSWORD=dev_pw
DB_HOST=localhost
DB_PORT=5432
DB_NAME=brainrot_news_reels
```

### Step 2: Verify .env is in .gitignore

Ensure `.env` is listed in `.gitignore` to prevent committing sensitive credentials.

---

## Verification

### Test Database Connection

**Using psql:**
```bash
psql -U dev_user -d brainrot_news_reels -h localhost
```

Enter password when prompted: `dev_pw`

In psql, verify tables exist (after running the app):
```sql
\dt
\q
```

### Test from Python

```bash
cd /path/to/brainrot-news-reels
source venv/bin/activate  # or activate your virtual environment
python -c "from backend.database import engine; from sqlalchemy import text; conn = engine.connect(); print('Connection successful!'); conn.close()"
```

### Test from FastAPI App

Start the server:
```bash
uvicorn backend.main:app --reload
```

The app will automatically create tables on startup. Check the logs for any connection errors.

---

## Troubleshooting

### macOS

**Issue: `psql: command not found`**
- Solution: Add PostgreSQL to PATH (see Step 4 in macOS setup)
- Verify: `which psql` should show a path
- Alternative: Use full path: `/opt/homebrew/opt/postgresql@16/bin/psql`

**Issue: Service won't start**
```bash
brew services list | grep postgresql
brew services restart postgresql@16
tail -f /opt/homebrew/var/log/postgresql@16.log
```

**Issue: Port 5432 already in use**
```bash
lsof -i :5432
# Kill the process or change port in .env
```

### Windows

**Issue: `psql` not recognized**
- Solution: Restart Command Prompt/PowerShell after adding to PATH
- Verify PATH: `echo %PATH%` should include PostgreSQL bin directory

**Issue: Service not running**
```cmd
net start postgresql-x64-16
# Or check Services (services.msc)
```

**Issue: Authentication failed**
- Verify password is correct
- Check `pg_hba.conf` in PostgreSQL data directory (usually `C:\Program Files\PostgreSQL\16\data`)

### Linux

**Issue: Permission denied**
- Solution: Use `sudo -u postgres` to run psql commands
- Or configure password authentication in `pg_hba.conf`

**Issue: Service not running**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo journalctl -u postgresql -n 50  # View logs
```

**Issue: Connection refused**
- Check if PostgreSQL is listening: `sudo netstat -tlnp | grep 5432`
- Verify firewall settings
- Check `postgresql.conf` for `listen_addresses`

### General Issues

**Issue: `permission denied for schema public`**
```sql
-- Connect as superuser (postgres)
psql -U postgres -d brainrot_news_reels
GRANT ALL ON SCHEMA public TO dev_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dev_user;
```

**Issue: Database already exists**
```sql
DROP DATABASE IF EXISTS brainrot_news_reels;
CREATE DATABASE brainrot_news_reels;
```

**Issue: User already exists**
```sql
-- Option 1: Drop and recreate
DROP USER IF EXISTS dev_user;
CREATE USER dev_user WITH PASSWORD 'dev_pw';

-- Option 2: Change password
ALTER USER dev_user WITH PASSWORD 'dev_pw';
```

---

## Quick Reference Commands

### Start/Stop PostgreSQL

**macOS:**
```bash
brew services start postgresql@16
brew services stop postgresql@16
brew services restart postgresql@16
```

**Windows:**
```cmd
net start postgresql-x64-16
net stop postgresql-x64-16
```

**Linux:**
```bash
sudo systemctl start postgresql
sudo systemctl stop postgresql
sudo systemctl restart postgresql
```

### Connect to Database

```bash
psql -U dev_user -d brainrot_news_reels -h localhost
```

### Useful psql Commands

```sql
\l          -- List all databases
\dt         -- List all tables in current database
\du         -- List all users
\d table_name  -- Describe a table
\q          -- Quit psql
```

---

## Security Notes

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use strong passwords** in production environments
3. **Limit database user permissions** - Only grant necessary privileges
4. **Use environment variables** or secrets managers in production
5. **Enable SSL** for production database connections

---

## Next Steps

After setting up PostgreSQL:

1. Verify your `.env` file is configured correctly
2. Start your FastAPI application: `uvicorn backend.main:app --reload`
3. The application will automatically create all necessary tables on startup
4. Check the application logs to confirm successful database connection

For more information, see the main [README.md](README.md).
