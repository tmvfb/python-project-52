# django-task-manager
[![Website https://python-project-52-production-ae52.up.railway.app/](https://img.shields.io/website-up-down-green-red/https/python-project-52-production-ae52.up.railway.app.svg)](https://python-project-52-production-ae52.up.railway.app/)
[![Actions Status](https://github.com/tmvfb/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/tmvfb/python-project-52/actions)
[![Github Actions Status](https://github.com/tmvfb/python-project-52/workflows/Python%20CI/badge.svg)](https://github.com/tmvfb/python-project-52/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d9a8f7c4c888941fe195/test_coverage)](https://codeclimate.com/github/tmvfb/python-project-52/test_coverage)

## Description
This package is a task management system similar to http://www.redmine.org/. It allows users to create tasks, assign them to specific performers, change their statuses and tag them with specific labels. The app requires registration and authentication to access its features. Backend is written in Django, frontend utilizes Bootstrap.
  
**Key features:**
* User registration and authentication for secure access
* CRUD operations for users, labels, statuses, and tasks
* Permission system to control user actions on resources deletion
* Tasks filtering
* Site search
* 2 languages support
* Implementation of models and relationships using Django ORM
* Efficient form generation and error handling with Django's built-in form support
* Test written using Django unittest to ensure code functionality and reliability
* Integration of [Rollbar](https://rollbar.com/) for real-time error monitoring
  
  
**UI demo:**
  
![image](https://github.com/tmvfb/python-project-52/assets/116455436/fbb117e8-225a-4013-b9cf-f7449eacf14f)

## Prerequisites
* Python >=3.8.1
* pip >=22.0
* poetry >=1.4.0
* GNU make

## Installation (WSL/Linux)
```
$ git clone https://github.com/tmvfb/python-project-52.git
$ cd python-project-52.git
$ make install
```
Then configure environment variables below.  
Run `make dev` to start server.

## Environment variables
```
SECRET_KEY=
DATABASE_URL=                   (default is sqlite3 db in repository)
DJANGO_SETTINGS_MODULE=         (optional) 
DEBUG=                          (optional, default False) 
ROLLBAR_ACCESS_TOKEN=           (optional) 
```
