#!/bin/bash
# Health check script for Django application

set -e

# Check if Django is responding
python manage.py check --deploy --settings=pesonal_finance_manager.settings

# Try to connect to the database
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pesonal_finance_manager.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT 1')
print('Database connection successful')
"

echo "Health check passed"