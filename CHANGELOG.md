# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup

## [1.0.0] - 2025-09-04

### Added
- Complete Flask-based MFA/TOTP code generator application
- Docker containerization with persistent storage using Docker volumes
- SQLite database with automatic schema creation
- Modern responsive web UI built with Bootstrap 5
- Real-time TOTP code generation and auto-refresh
- QR code generation for easy authenticator app setup
- Click-to-copy functionality for TOTP codes
- Account management (add, edit, delete MFA accounts)
- Security-focused design with non-root Docker execution
- Environment-based configuration system
- Health checks and monitoring
- Comprehensive documentation (README.md, DOCKER.md)
- MIT License for open source usage
- Complete .gitignore for Python/Flask projects
- Docker Compose setup for easy deployment
- Environment variable template (.env.example)

### Security
- Non-root user execution in Docker containers
- Environment-based secret management
- Isolated Docker networking
- Secure handling of MFA secrets
- Production vs development configuration modes

### Documentation
- Comprehensive README with installation and usage instructions
- Docker deployment guide with troubleshooting
- Security best practices documentation
- Contributing guidelines
- API documentation

[Unreleased]: https://github.com/ifrizzell/mfa-manager/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ifrizzell/mfa-manager/releases/tag/v1.0.0
