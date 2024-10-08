#!/bin/bash

until pg_isready -h $GAME_HOST -p $POSTGRES_PORT -U $POSTGRES_USER
do
  echo "$(date) - waiting for database to start"
  sleep 2
done



python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations auth_app


python manage.py runserver 0.0.0.0:8001


