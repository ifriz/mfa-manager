# MFA Manager - Docker Deployment Guide

This guide explains how to deploy the MFA Manager application using Docker containers with persistent data storage.

## Quick Start

1. **Clone or download the project files**
2. **Start the application:**
   ```bash
   docker-compose up -d
   ```
3. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## Prerequisites

- Docker (version 20.0 or higher)
- Docker Compose (version 2.0 or higher)

## File Structure

```
mfa-manager/
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Service orchestration
├── .dockerignore           # Files excluded from Docker build
├── .env.example            # Environment variable template
├── app.py                  # Main Flask application
├── models.py               # Database models
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
└── DOCKER.md              # This file
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`) to customize the deployment:

```bash
# Copy the example environment file
cp .env.example .env
```

Key configuration options:

- `FLASK_ENV=production` - Set to production mode
- `SECRET_KEY` - Secure secret key for session management
- `DATABASE_PATH=/app/data/mfa_manager.db` - Database location within container

### Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Add the generated key to your `.env` file.

## Docker Compose Services

### Main Service: mfa-manager

- **Image**: Built from local Dockerfile
- **Port**: 5000 (mapped to host port 5000)
- **Volume**: `mfa_data` mounted at `/app/data` for database persistence
- **Network**: Isolated network `mfa-manager-network`
- **Health Check**: Automatic health monitoring
- **Restart Policy**: `unless-stopped`

## Volume Persistence

The application uses a Docker volume for database persistence:

- **Volume Name**: `mfa-manager-data`
- **Mount Point**: `/app/data` (inside container)
- **Content**: SQLite database file (`mfa_manager.db`)

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume details
docker volume inspect mfa-manager-data

# Backup database
docker exec mfa-manager cp /app/data/mfa_manager.db /tmp/backup.db
docker cp mfa-manager:/tmp/backup.db ./backup_$(date +%Y%m%d_%H%M%S).db

# View volume data location (Windows with WSL)
docker volume inspect mfa-manager-data --format '{{ .Mountpoint }}'
```

## Management Commands

### Start Services

```bash
# Start in background
docker-compose up -d

# Start with logs visible
docker-compose up

# Build and start (after code changes)
docker-compose up --build
```

### Monitor and Debug

```bash
# View service status
docker-compose ps

# View logs
docker-compose logs -f mfa-manager

# View real-time logs
docker-compose logs -f --tail=100 mfa-manager

# Execute command inside container
docker exec -it mfa-manager bash

# Access Python shell
docker exec -it mfa-manager python
```

### Stop and Cleanup

```bash
# Stop services (keeps volumes)
docker-compose down

# Stop and remove volumes (DANGER: deletes all data)
docker-compose down -v

# Remove unused images
docker image prune

# Complete cleanup (removes all containers, networks, images)
docker system prune -a
```

## Security Considerations

### Production Deployment

1. **Set a Secure Secret Key**:
   ```bash
   export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   ```

2. **Use HTTPS**: Deploy behind a reverse proxy (nginx, Traefik) with SSL
   
3. **Firewall Configuration**: Restrict access to port 5000

4. **Regular Backups**: Automated database backups

5. **Update Base Images**: Keep Docker images updated
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

### Network Security

The application runs in an isolated Docker network (`mfa-manager-network`). Only the web port (5000) is exposed to the host.

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "5001:5000"  # Use port 5001 instead
   ```

2. **Permission Issues**:
   ```bash
   # Check container logs
   docker-compose logs mfa-manager
   
   # Fix volume permissions
   docker exec -it mfa-manager chown -R mfa:mfa /app/data
   ```

3. **Database Corruption**:
   ```bash
   # Stop services
   docker-compose down
   
   # Remove volume (WARNING: deletes all data)
   docker volume rm mfa-manager-data
   
   # Restart (creates fresh database)
   docker-compose up -d
   ```

4. **SSL Certificate Issues** (during build):
   The Dockerfile includes trusted host flags for PyPI to handle corporate network SSL issues.

### Health Checks

The container includes automatic health monitoring:

```bash
# Check health status
docker inspect mfa-manager --format='{{.State.Health.Status}}'

# View health check logs
docker inspect mfa-manager --format='{{range .State.Health.Log}}{{.Output}}{{end}}'
```

## Backup and Restore

### Backup Database

```bash
# Create backup script
cat > backup_mfa.sh << 'EOF'
#!/bin/bash
BACKUP_FILE="mfa_backup_$(date +%Y%m%d_%H%M%S).db"
docker exec mfa-manager cp /app/data/mfa_manager.db /tmp/backup.db
docker cp mfa-manager:/tmp/backup.db "./$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"
EOF

chmod +x backup_mfa.sh
./backup_mfa.sh
```

### Restore Database

```bash
# Stop the application
docker-compose down

# Copy backup to volume
docker run --rm -v mfa-manager-data:/app/data -v $(pwd):/backup alpine cp /backup/your_backup.db /app/data/mfa_manager.db

# Start the application
docker-compose up -d
```

## Monitoring

### Resource Usage

```bash
# View container resource usage
docker stats mfa-manager

# View disk usage
docker system df

# View volume size
docker exec mfa-manager du -sh /app/data
```

## Updates

### Updating the Application

1. **Pull latest code**
2. **Rebuild and deploy**:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

### Updating Base Images

```bash
# Update Python base image
docker pull python:3.11-slim

# Rebuild with new base
docker-compose build --no-cache
docker-compose up -d
```

---

## Support

For issues or questions:

1. Check container logs: `docker-compose logs mfa-manager`
2. Verify volume persistence: `docker volume ls`
3. Test connectivity: `curl http://localhost:5000`
4. Check health status: `docker-compose ps`

**Security Reminder**: This application handles sensitive MFA secrets. Always deploy securely and follow security best practices.
