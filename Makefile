MANAGE = python manage.py

run:
	$(MANAGE) runserver

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

worker:
	celery -A cinema worker --loglevel=info