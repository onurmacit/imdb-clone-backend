#!/bin/bash

set -e

echo "Waiting for database..."
./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up!"

if [ "$1" = "web" ]; then
    echo "Running migrations..."
    python manage.py migrate movies
    python manage.py migrate
    echo "Starting web server..."
    exec python manage.py runserver 0.0.0.0:8000
elif [ "$1" = "celery" ]; then
    echo "Starting celery worker..."
    exec celery -A imdb_clone.celery.app worker --loglevel=info
else
    echo "Invalid argument provided. Use 'web' or 'celery'."
    exit 1
fi
