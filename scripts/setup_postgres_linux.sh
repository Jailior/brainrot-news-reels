#!/bin/bash

# PostgreSQL Setup Script for Linux
# This script automates the setup of PostgreSQL database and user for Brainrot News Reels
# Supports Ubuntu/Debian and Fedora/RHEL/CentOS

set -e  # Exit on error

echo "========================================="
echo "PostgreSQL Setup for Brainrot News Reels"
echo "Linux Setup Script"
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

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo -e "${RED}Error: Cannot detect Linux distribution${NC}"
    exit 1
fi

echo -e "${YELLOW}Detected distribution: $DISTRO${NC}"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: This script must be run with sudo${NC}"
    echo "Usage: sudo ./setup_postgres_linux.sh"
    exit 1
fi

# Install PostgreSQL based on distribution
if [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
    echo -e "${YELLOW}Installing PostgreSQL for Ubuntu/Debian...${NC}"
    
    # Update package list
    apt update
    
    # Install PostgreSQL
    if ! command -v psql &> /dev/null; then
        apt install -y postgresql postgresql-contrib
        echo -e "${GREEN}✓${NC} PostgreSQL installed"
    else
        echo -e "${GREEN}✓${NC} PostgreSQL is already installed"
    fi
    
    # Start and enable service
    systemctl start postgresql
    systemctl enable postgresql
    
elif [[ "$DISTRO" == "fedora" || "$DISTRO" == "rhel" || "$DISTRO" == "centos" ]]; then
    echo -e "${YELLOW}Installing PostgreSQL for Fedora/RHEL/CentOS...${NC}"
    
    # Install PostgreSQL
    if ! command -v psql &> /dev/null; then
        dnf install -y postgresql-server postgresql
        echo -e "${GREEN}✓${NC} PostgreSQL installed"
        
        # Initialize database
        postgresql-setup --initdb
        echo -e "${GREEN}✓${NC} Database initialized"
    else
        echo -e "${GREEN}✓${NC} PostgreSQL is already installed"
    fi
    
    # Start and enable service
    systemctl start postgresql
    systemctl enable postgresql
else
    echo -e "${YELLOW}Unsupported distribution. Please install PostgreSQL manually.${NC}"
    exit 1
fi

# Wait for PostgreSQL to be ready
echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
sleep 3

# Verify PostgreSQL is running
if systemctl is-active --quiet postgresql; then
    echo -e "${GREEN}✓${NC} PostgreSQL service is running"
else
    echo -e "${RED}Error: PostgreSQL service is not running${NC}"
    exit 1
fi

echo -e "${YELLOW}Creating database and user...${NC}"

# Create database and user
sudo -u postgres psql <<EOF
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
sudo -u postgres psql -d "$DB_NAME" <<EOF
GRANT ALL ON SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO $DB_USER;
EOF

echo -e "${GREEN}✓${NC} Schema permissions granted"

# Configure pg_hba.conf for password authentication (if needed)
echo -e "${YELLOW}Checking authentication configuration...${NC}"
PG_HBA_PATH=$(sudo -u postgres psql -t -P format=unaligned -c 'SHOW hba_file;')

if [ -f "$PG_HBA_PATH" ]; then
    # Check if local connections are set to trust or md5
    if grep -q "local.*all.*all.*trust" "$PG_HBA_PATH"; then
        echo -e "${GREEN}✓${NC} Authentication configured (trust for local)"
    elif grep -q "local.*all.*all.*md5" "$PG_HBA_PATH"; then
        echo -e "${GREEN}✓${NC} Authentication configured (md5 for local)"
    else
        echo -e "${YELLOW}⚠${NC}  You may need to configure pg_hba.conf for password authentication"
    fi
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
echo "Note: You may need to configure pg_hba.conf if you encounter"
echo "authentication issues. See POSTGRESQL_SETUP.md for details."
echo ""
