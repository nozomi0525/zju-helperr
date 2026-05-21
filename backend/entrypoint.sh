#!/bin/sh
set -e

echo "Making migrations and running migrate..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn campus_help.wsgi:application --bind 0.0.0.0:8000 --workers 1
