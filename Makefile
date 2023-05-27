dev:
	python3.8 manage.py runserver

start:
	poetry run gunicorn task_manager.wsgi

selfcheck:
	poetry check

sort:
	isort .

test:
	python3.8 manage.py test

lint:
	poetry run flake8 task_manager

activate:
	poetry shell

check: sort selfcheck test lint

shell:
	django-admin shell

trans:
	django-admin makemessages -l ru

compile:
	django-admin compilemessages

.PHONY: dev start selfcheck test lint activate check shell trans compile sort
