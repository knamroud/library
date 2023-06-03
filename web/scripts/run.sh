#!/bin/bash
pipenv run python3 manage.py makemigrations
pipenv run python3 manage.py migrate
if [ "$PRODUCTION" -eq "0" ]; then
    pipenv run python3 manage.py runserver 0.0.0.0:8000
else 
    echo "not yet"
fi