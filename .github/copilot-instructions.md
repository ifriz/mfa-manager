# Copilot Instructions for MFA Manager

## Project Overview
- **MFA Manager** is a Flask web app for managing TOTP-based MFA secrets and generating codes. It is designed for local or team use, with a focus on security and ease of use.
- Data is stored in a local SQLite database (`mfa_manager.db` by default), with Docker support for persistent storage.
- The UI is built with Bootstrap and supports QR code generation, account management, and real-time TOTP updates.

## Key Files & Structure
- `app.py`: Main Flask app, routes, and app setup
- `models.py`: SQLAlchemy models (notably `mfa_accounts`)
- `config.py`: Handles environment variables and config
- `run.py`: Entrypoint for running the app
- `templates/`: Jinja2 HTML templates for all UI pages
- `static/`: Static assets (CSS, JS, images)
- `requirements.txt`: Python dependencies
- `docker-compose.yml`, `Dockerfile`: Containerization and orchestration

## Developer Workflows
- **Run locally:**
  - `python -m venv venv && venv\Scripts\activate` (Windows)
  - `pip install -r requirements.txt`
  - `python run.py`
- **Run with Docker:**
  - `docker-compose up -d` (persistent data in Docker volume)
- **Change port:**
  - Set `PORT` or `FLASK_PORT` env var, or edit `.env` file
- **Test:**
  - (If present) Run `pytest` or `python -m unittest` (see `test_*.py` files)
- **Debug:**
  - Set `FLASK_ENV=development` for debug mode
  - Use `docker-compose logs -f mfa-manager` for container logs

## Project Conventions & Patterns
- **Account data**: Managed via SQLAlchemy, all logic in `models.py` and `app.py`
- **Secrets**: Never hardcode; always use environment variables for `SECRET_KEY` and DB path
- **API**: REST endpoints under `/api/` (see README for details)
- **UI**: All user-facing pages use `base.html` as a template root
- **Port**: Defaults to 4570, but can be overridden
- **Security**: Always recommend HTTPS in production, and strong `SECRET_KEY`

## Integration & Extensibility
- **API endpoints**: `/api/codes`, `/api/code/<account_id>` for TOTP integration
- **Database**: Default is SQLite, but can be swapped via `DATABASE_URL` env var
- **Docker**: Persistent data via `mfa-manager-data` volume at `/app/data`

## Examples
- To add a new page, create a template in `templates/`, add a route in `app.py`, and (if needed) update the model in `models.py`.
- To change the database, set `DATABASE_URL` in the environment or `.env` file.

## References
- See `README.md` for full setup, usage, and troubleshooting
- See `DOCKER.md` for advanced Docker usage and backup/restore

---
**Security Reminder:** This app manages sensitive secrets. Always use secure deployment practices and never expose secrets in code or logs.
