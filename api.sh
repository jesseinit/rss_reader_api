#!/bin/bash
python manage.py migrate --noinput                # Apply database migrations
python manage.py collectstatic --clear --noinput  # Collect static files

# Test if PORT is set or set it
if [ -z "${PORT:-}" ]; then export PORT="8005"; fi

celery -A config.celery_app worker -l INFO --concurrency 2 --beat &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --worker-class gevent --log-level=info config.wsgi:application --access-logfile -
