#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py shell < create_users.py
python manage.py runserver 0.0.0.0:8000
