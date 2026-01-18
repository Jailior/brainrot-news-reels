# PostgreSQL Setup Script for Windows
# This script automates the setup of PostgreSQL database and user for Brainrot News Reels
# Run this script in PowerShell as Administrator

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Setup for Brainrot News Reels" -ForegroundColor Cyan
Write-Host "Windows Setup Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$DB_NAME = "brainrot_news_reels"
$DB_USER = "dev_user"
$DB_PASSWORD = "dev_pw"
$PG_VERSION = "16"

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Error: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Check if PostgreSQL is installed
$psqlPath = Get-Command psql -ErrorAction SilentlyContinue

if (-not $psqlPath) {
    Write-Host "PostgreSQL not found in PATH." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please install PostgreSQL first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    Write-Host "2. Run the installer" -ForegroundColor Yellow
    Write-Host "3. Remember the password you set for the 'postgres' user" -ForegroundColor Yellow
    Write-Host "4. Add PostgreSQL to PATH (or restart this script after installation)" -ForegroundColor Yellow
    Write-Host ""
    
    $install = Read-Host "Have you installed PostgreSQL? (y/n)"
    if ($install -ne "y") {
        Write-Host "Please install PostgreSQL and run this script again." -ForegroundColor Red
        exit 1
    }
    
    # Try to find PostgreSQL in common locations
    $commonPaths = @(
        "C:\Program Files\PostgreSQL\$PG_VERSION\bin",
        "C:\Program Files\PostgreSQL\15\bin",
        "C:\Program Files\PostgreSQL\14\bin"
    )
    
    $found = $false
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $env:Path += ";$path"
            Write-Host "Added to PATH: $path" -ForegroundColor Green
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "Could not find PostgreSQL installation." -ForegroundColor Red
        Write-Host "Please add PostgreSQL bin directory to PATH manually." -ForegroundColor Yellow
        exit 1
    }
    
    # Verify psql is now available
    $psqlPath = Get-Command psql -ErrorAction SilentlyContinue
    if (-not $psqlPath) {
        Write-Host "Error: psql still not found. Please restart PowerShell after adding to PATH." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ PostgreSQL found: $($psqlPath.Source)" -ForegroundColor Green

# Check if PostgreSQL service is running
$service = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue | Select-Object -First 1

if ($service) {
    if ($service.Status -eq "Running") {
        Write-Host "✓ PostgreSQL service is running" -ForegroundColor Green
    } else {
        Write-Host "Starting PostgreSQL service..." -ForegroundColor Yellow
        Start-Service -Name $service.Name
        Start-Sleep -Seconds 3
        Write-Host "✓ PostgreSQL service started" -ForegroundColor Green
    }
} else {
    Write-Host "Warning: Could not find PostgreSQL service" -ForegroundColor Yellow
    Write-Host "Please ensure PostgreSQL is installed and running" -ForegroundColor Yellow
}

# Prompt for postgres user password
Write-Host ""
Write-Host "Enter the password for the 'postgres' superuser:" -ForegroundColor Yellow
$postgresPassword = Read-Host -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($postgresPassword)
$plainPostgresPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "Creating database and user..." -ForegroundColor Yellow

# Create database and user
$env:PGPASSWORD = $plainPostgresPassword

# Create database if it doesn't exist
$dbExists = psql -U postgres -lqt | Select-String -Pattern "^\s*$DB_NAME\s"
if (-not $dbExists) {
    psql -U postgres -c "CREATE DATABASE $DB_NAME;" 2>&1 | Out-Null
    Write-Host "✓ Database created" -ForegroundColor Green
} else {
    Write-Host "✓ Database already exists" -ForegroundColor Green
}

# Create user if it doesn't exist
$userExists = psql -U postgres -t -c "SELECT 1 FROM pg_user WHERE usename = '$DB_USER';" 2>&1
if ($userExists -match "^\s*$") {
    psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>&1 | Out-Null
    Write-Host "✓ User created" -ForegroundColor Green
} else {
    psql -U postgres -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>&1 | Out-Null
    Write-Host "✓ User password updated" -ForegroundColor Green
}

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>&1 | Out-Null
Write-Host "✓ Privileges granted" -ForegroundColor Green

# Grant schema permissions
Write-Host "Granting schema permissions..." -ForegroundColor Yellow
psql -U postgres -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $DB_USER;" 2>&1 | Out-Null
psql -U postgres -d $DB_NAME -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;" 2>&1 | Out-Null
psql -U postgres -d $DB_NAME -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;" 2>&1 | Out-Null
psql -U postgres -d $DB_NAME -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO $DB_USER;" 2>&1 | Out-Null
Write-Host "✓ Schema permissions granted" -ForegroundColor Green

# Clear password from environment
Remove-Item Env:\PGPASSWORD

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Database Configuration:" -ForegroundColor Yellow
Write-Host "  Database: $DB_NAME"
Write-Host "  User: $DB_USER"
Write-Host "  Password: $DB_PASSWORD"
Write-Host "  Host: localhost"
Write-Host "  Port: 5432"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create a .env file in the project root with:"
Write-Host "   DB_USER=$DB_USER"
Write-Host "   DB_PASSWORD=$DB_PASSWORD"
Write-Host "   DB_HOST=localhost"
Write-Host "   DB_PORT=5432"
Write-Host "   DB_NAME=$DB_NAME"
Write-Host ""
Write-Host "2. Start your FastAPI application:"
Write-Host "   uvicorn backend.main:app --reload"
Write-Host ""
