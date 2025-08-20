#!/bin/bash

# Docker Setup Verification Script
# This script verifies that Docker support has been properly implemented

echo "=== Moneta Docker Setup Verification ==="
echo

# Check if Docker is available
echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed: $(docker --version)"
else
    echo "✗ Docker is not installed"
    exit 1
fi

# Check if Docker Compose is available
echo "2. Checking Docker Compose..."
if docker compose version &> /dev/null; then
    echo "✓ Docker Compose is available: $(docker compose version)"
else
    echo "✗ Docker Compose is not available"
    exit 1
fi

# Check for required files
echo "3. Checking Docker configuration files..."
required_files=(
    "Dockerfile"
    "docker-compose.yml"
    "docker-compose.dev.yml"
    "docker-compose.prod.yml"
    "docker-entrypoint.sh"
    ".dockerignore"
    ".env.example"
    "nginx.conf"
    "Makefile"
    "DOCKER.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file is missing"
        exit 1
    fi
done

# Check if .env file exists
echo "4. Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✓ .env file exists"
else
    echo "! .env file not found, creating from template..."
    cp .env.example .env
    echo "✓ Created .env from template"
fi

# Test database service startup
echo "5. Testing database service..."
echo "Starting PostgreSQL container..."
docker compose -f docker-compose.dev.yml up -d db

# Wait for database to be ready
echo "Waiting for database to be ready..."
for i in {1..30}; do
    if docker compose -f docker-compose.dev.yml exec -T db pg_isready -U postgres &> /dev/null; then
        echo "✓ Database is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "✗ Database failed to start within 30 seconds"
        docker compose -f docker-compose.dev.yml logs db
        exit 1
    fi
    sleep 1
done

# Clean up
echo "6. Cleaning up test containers..."
docker compose -f docker-compose.dev.yml down &> /dev/null
echo "✓ Test containers stopped"

echo
echo "=== Docker Setup Verification Complete ==="
echo "✓ All Docker components are properly configured"
echo
echo "Next steps:"
echo "1. Configure your .env file with your specific settings"
echo "2. Run 'make up-dev' to start the development environment"
echo "3. Access the application at http://localhost:8000"
echo
echo "For detailed instructions, see README.md or DOCKER.md"