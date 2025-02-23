#!/bin/bash

set -e

echo "Waiting for database..."
./wait-for-it.sh $DB_HOST:$DB_PORT --timeout=30 --strict -- echo "Database is up!"

echo "Running migrations..."
python manage.py migrate

if [ "$1" = "celery" ]; then
    echo "Starting celery worker..."
    exec celery -A imdb_clone worker --loglevel=info
else
    echo "Starting web server..."
    exec python manage.py runserver 0.0.0.0:8000
fi
