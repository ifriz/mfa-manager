# Copilot Instructions for MFA Manager

## Project Architecture
- **MFA Manager** is a Flask web app for managing TOTP-based MFA secrets and generating codes, designed for local/team use with a focus on security and usability.
- **Data Flow:**
  - User interacts with Flask routes in `app.py` (UI and REST API under `/api/`)
  - Account data is managed via SQLAlchemy models in `models.py` (notably `mfa_accounts`)
  - TOTP secrets are stored in a local SQLite DB (`mfa_manager.db` by default, path configurable)
  - UI is rendered with Jinja2 templates in `templates/` (all pages inherit from `base.html`)
  - Static assets (CSS/JS) are in `static/`
  - QR code generation and real-time TOTP updates are supported in the UI

## Key Files & Structure
- `app.py`: Main Flask app, all routes (UI/API), app setup, and business logic
- `models.py`: SQLAlchemy models and DB logic
- `config.py`: Loads environment variables and config (never hardcode secrets)
- `run.py`: Entrypoint for running the app (calls Flask)
- `templates/`: Jinja2 HTML templates (all pages extend `base.html`)
- `static/`: Static assets (CSS, JS, images)
- `requirements.txt`: Python dependencies
- `docker-compose.yml`, `Dockerfile`: Containerization and persistent storage

## Developer Workflows
- **Local run:**
  - `python -m venv venv && venv\Scripts\activate` (Windows)
  - `pip install -r requirements.txt`
  - `python run.py` (Flask app, default port 4570)
- **Docker run:**
  - `docker-compose up -d` (persistent data in Docker volume)
- **Change port:**
  - Set `PORT` or `FLASK_PORT` env var, or edit `.env`
- **Testing:**
  - Run `pytest` or `python -m unittest` (see `test_*.py`)
- **Debugging:**
  - Set `FLASK_ENV=development` for debug mode
  - Use `docker-compose logs -f mfa-manager` for container logs

## Project Conventions & Patterns
- **Account data:** All DB logic in `models.py`, all Flask routes in `app.py`
- **Secrets:** Always use env vars for `SECRET_KEY` and DB path (see `config.py`)
- **API:** REST endpoints under `/api/` (e.g., `/api/codes`, `/api/code/<account_id>`, see `app.py`)
- **UI:** All user-facing pages extend `base.html` (see `templates/`)
- **Port:** Defaults to 4570, override via env var
- **Security:** Recommend HTTPS in production, strong `SECRET_KEY`, never expose secrets in code/logs

## Integration & Extensibility
- **API endpoints:** `/api/codes`, `/api/code/<account_id>` for TOTP integration
- **Database:** Default is SQLite, override with `DATABASE_URL` env var
- **Docker:** Persistent data via `mfa-manager-data` volume at `/app/data`

## Examples & Patterns
- To add a new page: create a template in `templates/`, add a route in `app.py`, update model in `models.py` if needed
- To change DB backend: set `DATABASE_URL` in env or `.env`
- To add API: add route under `/api/` in `app.py`

## References
- See `README.md` for setup, usage, troubleshooting
- See `DOCKER.md` for advanced Docker usage, backup/restore

---
**Security Reminder:** This app manages sensitive secrets. Use secure deployment practices and never expose secrets in code or logs.
