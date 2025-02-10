#!/bin/bash

set -e

echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database initialized!"

python manage.py migrate

exec python manage.py runserver 0.0.0.0:8000
