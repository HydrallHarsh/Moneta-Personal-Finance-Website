#!/bin/bash
set -euo pipefail

echo "Building the project"

# Install project dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Running migrations"
python3 manage.py migrate

echo "Collect static files"
python3 manage.py collectstatic --noinput --clear
