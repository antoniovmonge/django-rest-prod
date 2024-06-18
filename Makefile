# Makefile

# Variables
MANAGE = docker compose -f docker-compose.local.yml run --rm django python manage.py
MANAGE_PROD = docker compose -f docker-compose.production.yml run --rm django python manage.py

# Commands
up:
	docker compose -f docker-compose.local.yml up

build:
	docker compose -f docker-compose.local.yml build

up-build:
	docker compose -f docker-compose.local.yml up --build

down:
	docker compose -f docker-compose.local.yml down

down-v:
	docker compose -f docker-compose.local.yml down -v

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

collectstatic:
	$(MANAGE) collectstatic

test:
	docker-compose -f docker-compose.local.yml run --rm django coverage run -m pytest

coverage:
	docker-compose -f docker-compose.local.yml run --rm django coverage html

shell:
	$(MANAGE) shell

shell_plus:
	$(MANAGE) shell_plus

prod-superuser:
	$(MANAGE_PROD) createsuperuser

superuser:
	$(MANAGE) createsuperuser

precommit:
	pre-commit run --all-files

show:
	docker compose -f docker-compose.local.yml ps

stop-django:
	docker-compose -f docker-compose.local.yml stop django
	docker rm -f core_local_django

start-django:
	docker-compose -f docker-compose.local.yml run --rm --service-ports django

isolate:
	docker-compose -f docker-compose.local.yml stop django
	docker-compose -f docker-compose.local.yml run --rm --service-ports django

debug:
	docker-compose -f docker-compose.local.yml stop django
	docker-compose -f docker-compose.local.yml run -T --rm --service-ports django pytest -s

flush:
	$(MANAGE) flush

users:
	$(MANAGE) create_local_user_and_admin

# Production
prod-build:
	docker compose -f docker-compose.production.yml build

prod-up:
	docker compose -f docker-compose.production.yml up

prod-down:
	docker compose -f docker-compose.production.yml down

prod-collectstatic:
	$(MANAGE_PROD) collectstatic

prod-migrate:
	$(MANAGE_PROD) makemigrations
	$(MANAGE_PROD) migrate

.PHONY: run migrate test shell superuser
