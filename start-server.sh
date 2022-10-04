#!/bin/sh

# Apply database migrations
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"

echo "Running tests.."
python manage.py test social_app.tests
echo "Starting server.."
gunicorn reunion.wsgi:application --bind :$PORT
