@echo off
REM PostgreSQL Setup Script for Windows (Batch)
REM This script automates the setup of PostgreSQL database and user for Brainrot News Reels
REM Run this script in Command Prompt as Administrator

echo =========================================
echo PostgreSQL Setup for Brainrot News Reels
echo Windows Setup Script (Batch)
echo =========================================
echo.

REM Configuration
set DB_NAME=brainrot_news_reels
set DB_USER=dev_user
set DB_PASSWORD=dev_pw
set PG_VERSION=16

REM Check if PostgreSQL is in PATH
where psql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PostgreSQL not found in PATH.
    echo.
    echo Please install PostgreSQL first:
    echo 1. Download from: https://www.postgresql.org/download/windows/
    echo 2. Run the installer
    echo 3. Remember the password you set for the 'postgres' user
    echo 4. Add PostgreSQL to PATH or restart this script after installation
    echo.
    
    REM Try to find PostgreSQL in common locations
    if exist "C:\Program Files\PostgreSQL\%PG_VERSION%\bin\psql.exe" (
        set "PATH=%PATH%;C:\Program Files\PostgreSQL\%PG_VERSION%\bin"
        echo Added PostgreSQL to PATH
    ) else if exist "C:\Program Files\PostgreSQL\15\bin\psql.exe" (
        set "PATH=%PATH%;C:\Program Files\PostgreSQL\15\bin"
        echo Added PostgreSQL to PATH
    ) else if exist "C:\Program Files\PostgreSQL\14\bin\psql.exe" (
        set "PATH=%PATH%;C:\Program Files\PostgreSQL\14\bin"
        echo Added PostgreSQL to PATH
    ) else (
        echo Error: Could not find PostgreSQL installation.
        echo Please add PostgreSQL bin directory to PATH manually.
        pause
        exit /b 1
    )
)

echo PostgreSQL found.
echo.

REM Check if PostgreSQL service is running
sc query postgresql-x64-%PG_VERSION% >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Checking PostgreSQL service...
    sc query postgresql-x64-%PG_VERSION% | find "RUNNING" >nul
    if %ERRORLEVEL% NEQ 0 (
        echo Starting PostgreSQL service...
        net start postgresql-x64-%PG_VERSION%
        timeout /t 3 /nobreak >nul
    )
    echo PostgreSQL service is running.
) else (
    echo Warning: Could not find PostgreSQL service.
    echo Please ensure PostgreSQL is installed and running.
)

echo.
echo Enter the password for the 'postgres' superuser:
set /p POSTGRES_PASSWORD=

echo.
echo Creating database and user...

REM Create database
psql -U postgres -c "CREATE DATABASE %DB_NAME%;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Database created.
) else (
    echo Database may already exist, continuing...
)

REM Create user
psql -U postgres -c "CREATE USER %DB_USER% WITH PASSWORD '%DB_PASSWORD%';" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo User created.
) else (
    psql -U postgres -c "ALTER USER %DB_USER% WITH PASSWORD '%DB_PASSWORD%';" 2>nul
    echo User password updated.
)

REM Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %DB_USER%;" 2>nul
echo Privileges granted.

REM Grant schema permissions
echo Granting schema permissions...
psql -U postgres -d %DB_NAME% -c "GRANT ALL ON SCHEMA public TO %DB_USER%;" 2>nul
psql -U postgres -d %DB_NAME% -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO %DB_USER%;" 2>nul
psql -U postgres -d %DB_NAME% -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO %DB_USER%;" 2>nul
psql -U postgres -d %DB_NAME% -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO %DB_USER%;" 2>nul
echo Schema permissions granted.

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Database Configuration:
echo   Database: %DB_NAME%
echo   User: %DB_USER%
echo   Password: %DB_PASSWORD%
echo   Host: localhost
echo   Port: 5432
echo.
echo Next steps:
echo 1. Create a .env file in the project root with:
echo    DB_USER=%DB_USER%
echo    DB_PASSWORD=%DB_PASSWORD%
echo    DB_HOST=localhost
echo    DB_PORT=5432
echo    DB_NAME=%DB_NAME%
echo.
echo 2. Start your FastAPI application:
echo    uvicorn backend.main:app --reload
echo.

pause
