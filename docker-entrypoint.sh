#!/bin/bash
export DJANGO_SETTINGS_MODULE="$MAIN.settings.production"

# Migrate the database first
echo "Migrating the database before starting the server"
echo "Apply database migrations"
python manage.py migrate

# Apply site migrations
echo "Apply site migrations"
python manage.py loaddata data/data.json

# Start Gunicorn processes
# Start server
echo "Starting server"
echo "Starting Gunicorn."
exec gunicorn --bind 0.0.0.0:$PORT $MAIN.wsgi:application