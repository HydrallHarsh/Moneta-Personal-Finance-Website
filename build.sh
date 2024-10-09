#!/bin/bash

echo "Building the project"

# Install pip if not installed
if ! command -v pip &> /dev/null
then
    echo "Installing pip"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py  # Clean up
fi

# Install project dependencies
python3 -m pip install -r requirements.txt

echo "Make migrations"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Collect static files"
python3 manage.py collectstatic --noinput --clear
