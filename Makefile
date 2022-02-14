COMPOSE = docker compose
SERVICE = web

start-local:
	python manage.py runserver 8005

start-docker:
	docker-compose up --build
