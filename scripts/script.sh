#!/bin/bash
set -e

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --clear --no-input
# python manage.py clear_cache 
python manage.py showmigrations
python manage.py runserver 0.0.0.0:8000