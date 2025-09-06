# 🛡️ MFA Manager - TOTP Code Generator

A secure, self-hosted Flask web application for managing Multi-Factor Authentication (MFA) secrets and generating Time-based One-Time Password (TOTP) codes. Perfect for individuals and teams who want to maintain control over their MFA tokens.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 🔐 **Secure TOTP Generation**: Generate 6-digit TOTP codes compatible with Google Authenticator, Authy, and other authenticator apps
- 🐳 **Docker Support**: Complete containerization with persistent data volumes
- 🗄️ **SQLite Database**: Local storage for MFA secrets and account information
- 📱 **QR Code Support**: Generate QR codes for easy setup with authenticator apps
- 🔄 **Auto-Refresh**: Real-time code updates with expiration timers
- 📋 **Click to Copy**: Easy copying of TOTP codes to clipboard
- ✏️ **Account Management**: Add, edit, and delete MFA accounts
- 🎨 **Modern UI**: Clean, responsive web interface built with Bootstrap
- 🛡️ **Security-First**: Non-root Docker execution, environment-based secrets
- 📊 **Health Monitoring**: Built-in health checks and monitoring

## 📚 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Docker (Recommended)](#docker-recommended)
  - [Python/Pip](#pythonpip)
- [Usage](#-usage)
- [Security](#-security-considerations)
- [API](#-api-endpoints)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

**Docker (Recommended):**
```bash
git clone <your-repo-url>
cd mfa-manager
docker-compose up -d
```

**Python/Pip:**
```bash
git clone <your-repo-url>
cd mfa-manager
pip install -r requirements.txt
python run.py
```

Then open `http://localhost:5000` in your browser.

## 💿 Installation

### Docker (Recommended)

The easiest way to run MFA Manager is using Docker with persistent data storage:

#### Prerequisites
- Docker 20.0+
- Docker Compose 2.0+

#### Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd mfa-manager
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   Open `http://localhost:5000` in your browser

4. **View logs (optional):**
   ```bash
   docker-compose logs -f mfa-manager
   ```

**Data Persistence:** Your MFA accounts are automatically saved in a Docker volume and will persist between container restarts.

### Python/Pip

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

#### Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd mfa-manager
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

## 📱 Usage

### Adding a New Account

1. Click "Add New Account" on the dashboard
2. Enter a unique account name (e.g., "Google", "GitHub", "AWS")
3. Enter the secret key provided by the service
4. Optionally, specify an issuer name
5. Click "Add Account"

### Getting Secret Keys

To get your secret key from various services:

1. Go to your account's 2FA/MFA settings
2. Choose "Set up authenticator app" or similar option
3. Look for "Can't scan QR code?" or "Manual entry" link
4. Copy the provided secret key (base32 string)

### Using TOTP Codes

- TOTP codes are displayed on the main dashboard
- Click any code to copy it to your clipboard
- Codes refresh automatically every 30 seconds
- Color coding indicates when codes are about to expire

### Managing Accounts

- **View Details**: Click on an account name to see full details including QR code
- **Edit Account**: Modify account name, secret, or issuer
- **Delete Account**: Remove accounts you no longer need (with confirmation)

## 🛡️ Security Considerations

⚠️ **Important Security Notes:**

- **Keep Secret Keys Secure**: Anyone with access to your secret keys can generate your TOTP codes
- **Use HTTPS in Production**: For production deployment, always use HTTPS
- **Secure Your Device**: Run this application only on trusted, secure devices
- **Backup Safely**: If backing up secrets, ensure backups are encrypted
- **Environment Variables**: Set a custom `SECRET_KEY` environment variable in production

### Production Security

For production use, consider these additional security measures:

```bash
# Set a secure secret key
export SECRET_KEY="your-very-long-random-secret-key-here"

# Use a more secure database (PostgreSQL, MySQL)
export DATABASE_URL="postgresql://user:password@localhost/mfa_manager"
```

## Database

The application uses SQLite by default with the following schema:

- **mfa_accounts** table:
  - `id`: Primary key
  - `account_name`: Unique account identifier
  - `secret`: Base32-encoded TOTP secret
  - `issuer`: Organization or service name
  - `created_at`: Account creation timestamp
  - `updated_at`: Last modification timestamp

Database file location: `mfa_manager.db` in the project directory.

## 🔌 API Endpoints

The application provides REST API endpoints for integration:

- `GET /api/codes` - Get all current TOTP codes
- `GET /api/code/<account_id>` - Get TOTP code for specific account

## File Structure

```
mfa-manager/
├── app.py              # Main Flask application
├── models.py           # Database models
├── run.py              # Application runner script
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── mfa_manager.db     # SQLite database (created on first run)
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_account.html
│   ├── edit_account.html
│   ├── account_detail.html
│   ├── 404.html
│   └── 500.html
└── static/            # Static files (currently empty)
```

## Dependencies

- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **pyotp**: TOTP/HOTP library
- **qrcode**: QR code generation
- **Pillow**: Image processing for QR codes
- **cryptography**: Cryptographic functions

## Troubleshooting

### Common Issues

1. **Invalid Secret Format**: Ensure the secret is a valid base32 string
2. **Port Already in Use**: Change the port in `run.py` if 5000 is occupied
3. **Database Errors**: Delete `mfa_manager.db` to reset the database
4. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Getting Help

- Check the console output for error messages
- Verify that all dependencies are properly installed
- Ensure Python 3.7+ is being used
- Check that no firewall is blocking port 5000

## License

This project is for educational and personal use. Please ensure compliance with your organization's security policies before using in a work environment.

## 🔧 Development

### Project Structure

```
mfa-manager/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Service orchestration
├── .dockerignore           # Files excluded from Docker build
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore patterns
├── README.md               # This file
├── DOCKER.md               # Docker deployment guide
└── templates/              # HTML templates (if present)
    ├── base.html
    ├── index.html
    ├── add_account.html
    └── ...
```

### Development Setup

1. **Fork and clone the repository**
2. **Set up development environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run in development mode:**
   ```bash
   export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
   python run.py
   ```

4. **Test your changes:**
   ```bash
   # Run the application
   python run.py
   
   # Test with Docker
   docker-compose up --build
   ```

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep security considerations in mind

## 🚀 Contributing

We welcome contributions! Here's how to get started:

### Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? [Open an issue](../../issues)
- ✨ **Feature Requests**: Have an idea? [Request a feature](../../issues)
- 📝 **Documentation**: Improve docs, add examples
- 🔧 **Code**: Fix bugs, add features, improve performance
- 🛡️ **Security**: Report security issues responsibly

### Contribution Process

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly** (both Python and Docker modes)
5. **Commit your changes:** `git commit -m 'Add amazing feature'`
6. **Push to the branch:** `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Reporting Security Issues

Please report security vulnerabilities responsibly. Do not open public issues for security problems. Instead:

- Email security issues to the maintainer
- Provide detailed steps to reproduce
- Allow time for fixes before disclosure

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

✅ **You can:**
- Use commercially
- Modify and distribute
- Use privately
- Sublicense

⚠️ **You must:**
- Include the license and copyright notice

❌ **You cannot:**
- Hold the author liable

---

## 🔍 Additional Resources

- [🐳 Docker Deployment Guide](DOCKER.md)
- [🔒 Security Best Practices](https://owasp.org/www-project-cheat-sheets/cheatsheets/Authentication_Cheat_Sheet.html)
- [📱 TOTP RFC 6238](https://tools.ietf.org/html/rfc6238)
- [🛡️ Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)

---

**⚠️ Security Reminder**: This application handles sensitive MFA secrets. Always use it responsibly and on secure systems.
