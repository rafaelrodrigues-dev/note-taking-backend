#!/bin/sh

su-exec duser python manage.py collectstatic --noinput
su-exec duser python manage.py makemigrations --noinput
su-exec duser python manage.py migrate --noinput
exec su-exec duser gunicorn project.wsgi:application --bind 0.0.0.0:8000