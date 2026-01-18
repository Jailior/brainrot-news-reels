#!/bin/bash

# PostgreSQL Setup Script for macOS
# This script automates the setup of PostgreSQL database and user for Brainrot News Reels

set -e  # Exit on error

echo "========================================="
echo "PostgreSQL Setup for Brainrot News Reels"
echo "macOS Setup Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="brainrot_news_reels"
DB_USER="dev_user"
DB_PASSWORD="dev_pw"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo -e "${RED}Error: Homebrew is not installed.${NC}"
    echo "Please install Homebrew first:"
    echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo -e "${GREEN}✓${NC} Homebrew is installed"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL not found. Installing PostgreSQL@16...${NC}"
    brew install postgresql@16
    
    # Add to PATH
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
        export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
    else
        echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.bash_profile
        export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
    fi
    echo -e "${GREEN}✓${NC} PostgreSQL installed and added to PATH"
else
    echo -e "${GREEN}✓${NC} PostgreSQL is already installed"
    # Ensure PostgreSQL is in PATH
    if [[ "$SHELL" == *"zsh"* ]]; then
        if ! grep -q "postgresql@16/bin" ~/.zshrc 2>/dev/null; then
            echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
        fi
        export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
    fi
fi

# Start PostgreSQL service
echo -e "${YELLOW}Starting PostgreSQL service...${NC}"
brew services start postgresql@16 || brew services restart postgresql@16
sleep 2
echo -e "${GREEN}✓${NC} PostgreSQL service started"

# Wait for PostgreSQL to be ready
echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
for i in {1..30}; do
    if psql -U $(whoami) -d postgres -c "SELECT 1" &> /dev/null; then
        break
    fi
    sleep 1
done

# Get current user (macOS username)
CURRENT_USER=$(whoami)

echo -e "${YELLOW}Creating database and user...${NC}"

# Create database and user
psql -U "$CURRENT_USER" -d postgres <<EOF
-- Create database if it doesn't exist
SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Create user if it doesn't exist
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    ELSE
        ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

echo -e "${GREEN}✓${NC} Database and user created"

# Grant schema permissions
echo -e "${YELLOW}Granting schema permissions...${NC}"
psql -U "$CURRENT_USER" -d "$DB_NAME" <<EOF
GRANT ALL ON SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO $DB_USER;
EOF

echo -e "${GREEN}✓${NC} Schema permissions granted"

# Verify connection
echo -e "${YELLOW}Verifying connection...${NC}"
if psql -U "$DB_USER" -d "$DB_NAME" -h localhost -c "SELECT current_database(), current_user;" &> /dev/null; then
    echo -e "${GREEN}✓${NC} Connection verified successfully"
else
    echo -e "${YELLOW}⚠${NC}  Could not verify connection with new user (this is normal if password auth is required)"
fi

echo ""
echo "========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================="
echo ""
echo "Database Configuration:"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo "  Host: localhost"
echo "  Port: 5432"
echo ""
echo "Next steps:"
echo "1. Create a .env file in the project root with:"
echo "   DB_USER=$DB_USER"
echo "   DB_PASSWORD=$DB_PASSWORD"
echo "   DB_HOST=localhost"
echo "   DB_PORT=5432"
echo "   DB_NAME=$DB_NAME"
echo ""
echo "2. Start your FastAPI application:"
echo "   uvicorn backend.main:app --reload"
echo ""
