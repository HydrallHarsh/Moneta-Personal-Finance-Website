#!/bin/bash

# Exit on any failure
set -e

echo "Starting Docker entrypoint..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h ${DB_HOST:-db} -p ${DB_PORT:-5432} -U ${DB_USER:-postgres}; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "PostgreSQL is up - continuing..."

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations --noinput || echo "No new migrations"
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Build CSS in background if npm is available and src/styles.css exists
if [ -f "src/styles.css" ] && command -v npm &> /dev/null; then
    echo "Building CSS with Tailwind..."
    npm run build:css &
fi

# Create superuser if it doesn't exist (only in development)
if [ "${DEBUG:-True}" = "True" ]; then
    echo "Creating superuser if it doesn't exist..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF
fi

# Execute the main command
echo "Starting application..."
exec "$@"