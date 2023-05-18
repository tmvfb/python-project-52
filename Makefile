PORT ?= 8000

dev:
	python3.8 manage.py runserver

start:
	poetry run gunicorn task_manager.wsgi