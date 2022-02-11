COMPOSE = docker compose
SERVICE = web

start:
	python manage.py runserver

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up

up-d:
	$(COMPOSE) up -d

enter:
	$(COMPOSE) exec $(SERVICE) bash

createsuperuser:
	$(COMPOSE) exec $(SERVICE) python manage.py createsuperuser

pre-commit:
	pre-commit run --all-files

populate-history:
	$(COMPOSE) exec $(SERVICE) python manage.py populate_history --auto

shell:
	$(COMPOSE) exec $(SERVICE) python manage.py shell

test:
	$(COMPOSE) run --rm $(SERVICE) pytest -vv

down:
	$(COMPOSE) down

migrate:
	$(COMPOSE) exec $(SERVICE) python manage.py migrate

migrations:
	$(COMPOSE) exec $(SERVICE) python manage.py makemigrations

showmigrations:
	$(COMPOSE) exec $(SERVICE) python manage.py showmigrations

seed-category:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata projects_category_seed

seed-business-models:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata business_model_seed

seed-projects:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata projects_seed

seed-project-images:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata projects_images_seed

seed-users:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata users_seed

seed-consumers-waitlist:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata consumers_waitlist_seed

seed-supporters-waitlist:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata supporters_waitlist_seed

seed-providers-waitlist:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata provider_type_seed
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata providers_waitlist_seed
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata oemi_waitlist_seed
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata disi_waitlist_seed

seed-technologies:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata technologies_seed

seed-appliances:
	$(COMPOSE) exec $(SERVICE) python manage.py loaddata appliances_seed

seed-all: seed-category seed-business-models seed-projects seed-users seed-consumers-waitlist seed-supporters-waitlist seed-project-images seed-providers-waitlist seed-technologies seed-appliances
