# 🚀 Getting Started with MFA Manager

Welcome to MFA Manager! This guide will help you get up and running quickly.

## 📋 Prerequisites

Choose your preferred deployment method:

### Option A: Docker (Recommended)
- Docker 20.0+
- Docker Compose 2.0+

### Option B: Python/Pip
- Python 3.7+
- pip package manager

## ⚡ Quick Start

### Using Docker (Easiest)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mfa-manager.git
   cd mfa-manager
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Open in browser:**
   Navigate to `http://localhost:5000`

4. **Add your first MFA account:**
   - Click "Add New Account"
   - Enter account name (e.g., "Google", "GitHub")
   - Enter your secret key from the service
   - Click "Add Account"

### Using Python/Pip

1. **Clone and setup:**
   ```bash
   git clone https://github.com/yourusername/mfa-manager.git
   cd mfa-manager
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

3. **Open in browser:**
   Navigate to `http://127.0.0.1:5000`

## 🔑 Getting Your Secret Keys

Most services provide MFA secret keys when setting up two-factor authentication:

1. **Go to your account's security/2FA settings**
2. **Choose "Setup Authenticator App"**
3. **Look for "Can't scan QR code?" or "Manual entry"**
4. **Copy the secret key** (usually a long string of letters/numbers)
5. **Paste it into MFA Manager**

### Common Services

- **Google**: Account → Security → 2-Step Verification → Authenticator app
- **GitHub**: Settings → Security → Two-factor authentication
- **AWS**: IAM → Users → Security credentials → Assigned MFA device
- **Microsoft**: Security → Advanced security options → App passwords

## 🎯 Your First MFA Account

1. **Start with a test account** to get familiar with the interface
2. **Use the "Generate Secret" button** to create a test secret
3. **Verify the TOTP codes work** by comparing with another authenticator app
4. **Add your real accounts** once you're comfortable

## 🛡️ Security Best Practices

- ✅ **Run on a secure device** you trust
- ✅ **Use a strong SECRET_KEY** in production (see .env.example)
- ✅ **Keep your secret keys private** - they're as sensitive as passwords
- ✅ **Backup your database** regularly (Docker: backup the volume)
- ✅ **Use HTTPS** in production deployments
- ⚠️ **Never share your secret keys** or TOTP codes
- ⚠️ **Test thoroughly** before relying on it for important accounts

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f mfa-manager

# Stop services (keeps data)
docker-compose down

# Update application
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Backup database
docker exec mfa-manager cp /app/data/mfa_manager.db /tmp/backup.db
docker cp mfa-manager:/tmp/backup.db ./mfa_backup.db
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Important settings:
- `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
- `FLASK_ENV`: Set to `production` for production deployments
- `DATABASE_PATH`: Database location (Docker handles this automatically)

### Port Configuration

To use a different port, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Use port 8080 instead of 5000
```

## 📚 Need Help?

- 📖 **Full Documentation**: [README.md](README.md)
- 🐳 **Docker Guide**: [DOCKER.md](DOCKER.md)
- 🐛 **Report Issues**: [GitHub Issues](../../issues)
- 💡 **Request Features**: [GitHub Issues](../../issues)
- 🔒 **Security Issues**: Email maintainer directly

## 🎉 You're Ready!

Once you've added your first MFA account and generated some TOTP codes, you're all set! The application will automatically refresh codes every 30 seconds and show you when they're about to expire.

---

**Next Steps:**
- Explore the [full documentation](README.md)
- Set up [production deployment](DOCKER.md#production-deployment)
- Consider [contributing](README.md#contributing) to the project!
