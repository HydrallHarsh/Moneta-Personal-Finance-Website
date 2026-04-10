#!/bin/bash
set -euo pipefail

echo "Building the project"

# Vercel Python can be externally managed (PEP 668), so install deps in a local venv.
python3 -m venv .vercel_venv
PYTHON_BIN=".vercel_venv/bin/python"

# Install project dependencies
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt

if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
	echo "Running migrations"
	"$PYTHON_BIN" manage.py migrate
else
	echo "Skipping migrations (set RUN_MIGRATIONS=1 to enable)"
fi

echo "Collect static files"
"$PYTHON_BIN" manage.py collectstatic --noinput --clear
