# Docker Setup for Moneta Personal Finance Manager

This document provides comprehensive instructions for running the Moneta Personal Finance Manager using Docker.

## Quick Start

### Prerequisites
- Docker and Docker Compose installed on your system
- At least 2GB of free disk space
- Port 8000 (development) or port 80 (production) available

### Development Environment

1. **Clone and Setup Environment**
   ```bash
   git clone https://github.com/HydrallHarsh/Moneta-Personal-Finance-Website.git
   cd Moneta-Personal-Finance-Website
   cp .env.example .env
   ```

2. **Configure Environment Variables**
   Edit `.env` file with your settings:
   ```bash
   # Required: Set a secure secret key
   SECRET_KEY=your-super-secret-key-here-change-this-in-production
   
   # Optional: Email configuration for notifications
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

3. **Start Development Environment**
   ```bash
   # Using Docker Compose directly
   docker compose -f docker-compose.dev.yml up --build
   
   # Or using the Makefile
   make up-dev
   ```

4. **Access the Application**
   - Application: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - Default admin credentials: `admin` / `admin123`

### Production Environment

1. **Setup Environment for Production**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Start Production Environment**
   ```bash
   # With nginx reverse proxy
   docker compose -f docker-compose.prod.yml up -d --build
   
   # Or using the Makefile
   make up-prod
   ```

3. **Access the Application**
   - Application: http://localhost
   - Admin Panel: http://localhost/admin

## Available Docker Compose Files

### docker-compose.dev.yml
- **Purpose**: Development environment
- **Services**: Web application + PostgreSQL database
- **Features**: 
  - Hot reloading with volume mounts
  - Debug mode enabled
  - Direct access to port 8000
  - Automatic admin user creation

### docker-compose.yml
- **Purpose**: Standard environment with nginx
- **Services**: Web application + PostgreSQL + Redis + Nginx
- **Features**: 
  - Nginx reverse proxy
  - Static file serving
  - Redis for caching (future use)

### docker-compose.prod.yml
- **Purpose**: Production environment
- **Services**: Web application + PostgreSQL + Redis + Nginx
- **Features**: 
  - Optimized for production
  - Gunicorn WSGI server
  - Network isolation
  - Health checks

## Makefile Commands

The project includes a Makefile with convenient commands:

```bash
# Start services
make up          # Development mode
make up-prod     # Production mode with nginx

# Build images
make build       # Build Docker images

# Logs and monitoring
make logs        # Show all service logs
make logs-web    # Show only web service logs

# Database operations
make migrate     # Run database migrations
make createsuperuser  # Create Django admin user

# Utilities
make shell       # Open shell in web container
make down        # Stop all services
make clean       # Remove all containers and volumes
```

## Environment Variables

### Required Variables
- `SECRET_KEY`: Django secret key for security
- `DB_PASSWORD`: Database password (auto-generated if not set)

### Optional Variables
- `DEBUG`: Enable/disable debug mode (default: True in dev, False in prod)
- `DB_NAME`: Database name (default: moneta_db)
- `DB_USER`: Database username (default: postgres)
- `EMAIL_HOST_USER`: Gmail username for email notifications
- `EMAIL_HOST_PASSWORD`: Gmail app password
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Email Configuration

For email notifications to work:

1. Enable 2-factor authentication on your Gmail account
2. Generate an app-specific password
3. Use the app password in `EMAIL_HOST_PASSWORD`

Example:
```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
EMAIL_USE_TLS=True
EMAIL_PORT=587
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   sudo netstat -tulpn | grep :8000
   
   # Stop the Docker services
   make down
   ```

2. **Database Connection Issues**
   ```bash
   # Check database logs
   make logs-db
   
   # Restart the database service
   docker compose -f docker-compose.dev.yml restart db
   ```

3. **Static Files Not Loading**
   ```bash
   # Collect static files manually
   make collectstatic
   
   # Or restart the web service
   docker compose -f docker-compose.dev.yml restart web
   ```

4. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Development Tips

1. **Database Access**
   ```bash
   # Connect to PostgreSQL directly
   docker compose -f docker-compose.dev.yml exec db psql -U postgres -d moneta_db
   ```

2. **Django Shell**
   ```bash
   # Access Django shell
   make shell
   python manage.py shell
   ```

3. **View Real-time Logs**
   ```bash
   # Follow all logs
   make logs
   
   # Follow only web service logs
   make logs-web
   ```

## Data Persistence

- **Database**: Data is persisted in Docker volumes
- **Media Files**: Uploaded files are stored in Docker volumes
- **Static Files**: Generated during container startup

### Backup and Restore

1. **Database Backup**
   ```bash
   docker compose -f docker-compose.dev.yml exec db pg_dump -U postgres moneta_db > backup.sql
   ```

2. **Database Restore**
   ```bash
   docker compose -f docker-compose.dev.yml exec -T db psql -U postgres moneta_db < backup.sql
   ```

## Performance Optimization

### Production Recommendations

1. **Use production environment variables**
2. **Set up proper SSL certificates for HTTPS**
3. **Configure nginx for static file caching**
4. **Monitor resource usage**
5. **Set up log rotation**

### Resource Limits

You can add resource limits to docker-compose files:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
```

## Security Considerations

1. **Change default passwords** before deploying to production
2. **Use environment-specific `.env` files**
3. **Don't commit `.env` files** to version control
4. **Set up proper firewall rules** for production deployment
5. **Regularly update Docker images** for security patches

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Docker logs: `make logs`
3. Check the project's GitHub issues
4. Ensure all prerequisites are met