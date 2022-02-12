COMPOSE = docker compose
SERVICE = web

start-dev:
	python manage.py runserver 8005

start-beat:
	celery -A config.celery_app beat -l INFO

start-worker:
	celery -A config.celery_app worker --beat -l INFO --concurrency 1
	# celery -A config.celery_app worker -l INFO --concurrency 1
