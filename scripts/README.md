# PostgreSQL Setup Scripts

This directory contains automated setup scripts for PostgreSQL on different platforms.

## Available Scripts

### macOS
- **`setup_postgres_macos.sh`** - Automated setup for macOS using Homebrew
  ```bash
  chmod +x setup_postgres_macos.sh
  ./setup_postgres_macos.sh
  ```

### Linux
- **`setup_postgres_linux.sh`** - Automated setup for Ubuntu/Debian and Fedora/RHEL/CentOS
  ```bash
  chmod +x setup_postgres_linux.sh
  sudo ./setup_postgres_linux.sh
  ```

### Windows
- **`setup_postgres_windows.ps1`** - PowerShell script (recommended)
  ```powershell
  # Run PowerShell as Administrator
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  .\setup_postgres_windows.ps1
  ```

- **`setup_postgres_windows.bat`** - Batch script (alternative)
  ```cmd
  REM Run Command Prompt as Administrator
  setup_postgres_windows.bat
  ```

## What These Scripts Do

All scripts perform the following tasks:

1. **Check/Install PostgreSQL** - Verify PostgreSQL is installed, install if needed
2. **Start PostgreSQL Service** - Ensure PostgreSQL is running
3. **Create Database** - Create `brainrot_news_reels` database
4. **Create User** - Create `dev_user` with password `dev_pw`
5. **Grant Permissions** - Grant all necessary permissions on database and schema
6. **Verify Setup** - Test the connection (where possible)

## Configuration

The scripts use the following default configuration:
- **Database Name**: `brainrot_news_reels`
- **Database User**: `dev_user`
- **Database Password**: `dev_pw`
- **Host**: `localhost`
- **Port**: `5432`

To change these values, edit the variables at the top of each script.

## Manual Setup

If you prefer to set up PostgreSQL manually, see the comprehensive guide in [POSTGRESQL_SETUP.md](../POSTGRESQL_SETUP.md).

## Troubleshooting

If you encounter issues:

1. **macOS**: Check that Homebrew is installed and PostgreSQL service is running
2. **Linux**: Ensure you're running with `sudo` privileges
3. **Windows**: Run PowerShell/CMD as Administrator

For detailed troubleshooting, see [POSTGRESQL_SETUP.md](../POSTGRESQL_SETUP.md#troubleshooting).
