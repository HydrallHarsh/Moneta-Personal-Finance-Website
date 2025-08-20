.PHONY: help build up up-prod up-dev down restart logs shell migrate collectstatic createsuperuser clean

# Default target
help:
	@echo "Available commands:"
	@echo "  build          Build Docker images"
	@echo "  up             Start all services (development)"
	@echo "  up-prod        Start all services (production with nginx)"
	@echo "  up-dev         Start development services (without nginx)"
	@echo "  down           Stop all services"
	@echo "  restart        Restart all services"
	@echo "  logs           Show logs for all services"
	@echo "  logs-web       Show logs for web service only"
	@echo "  shell          Open shell in web container"
	@echo "  migrate        Run database migrations"
	@echo "  collectstatic  Collect static files"
	@echo "  createsuperuser Create Django superuser"
	@echo "  clean          Remove all containers, volumes, and images"

# Build Docker images
build:
	docker-compose -f docker-compose.dev.yml build

# Start development services
up:
	docker-compose -f docker-compose.dev.yml up

# Start production services (with nginx)
up-prod:
	docker-compose -f docker-compose.prod.yml up -d

# Start development services (without nginx)
up-dev:
	docker-compose -f docker-compose.dev.yml up

# Stop all services
down:
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.prod.yml down

# Restart all services
restart:
	docker-compose -f docker-compose.dev.yml restart

# Show logs
logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Show web logs only
logs-web:
	docker-compose -f docker-compose.dev.yml logs -f web

# Open shell in web container
shell:
	docker-compose -f docker-compose.dev.yml exec web bash

# Run migrations
migrate:
	docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Collect static files
collectstatic:
	docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput

# Create superuser
createsuperuser:
	docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Clean everything
clean:
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans
	docker-compose -f docker-compose.prod.yml down -v --remove-orphans
	docker system prune -f
	docker volume prune -f