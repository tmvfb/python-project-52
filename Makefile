dev:
	python3.8 manage.py runserver

start:
	poetry run gunicorn task_manager.wsgi

selfcheck:
	poetry check

test:
	python3.8 manage.py test

lint:
	poetry run flake8 task_manager

activate:
	poetry shell

check: selfcheck test lint

shell:
	django-admin shell

.PHONY: dev start selfcheck test lint activate check shell
