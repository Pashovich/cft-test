#!/bin/sh
python3 main.py --load_env
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        echo $DATABASE_HOST $DATABASE_PORT
      sleep 1
    done

    echo "PostgreSQL started"
fi
alembic revision --autogenerate -m "init"
alembic upgrade head
pytest -v
python3 main.py