COMPOSE = docker compose
SERVICE = web

start-dev:
	python manage.py runserver 8005

start-beat:
	celery -A config.celery_app beat -l INFO

start-worker:
	celery -A config.celery_app worker --beat -l INFO --concurrency 1

start-prod:
	gunicorn --bind 0.0.0.0:8005 --workers 3 --worker-class gevent --log-level=info config.wsgi:application --access-logfile -

build:
	docker build -t rss_api . 

start:
	docker run --env-file .env --rm -p 8005:8005 rss_api
