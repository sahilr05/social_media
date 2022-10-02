#!/usr/bin/env bash
# start-server.sh

# Apply database migrations
echo "Apply database migrations.."
python manage.py migrate

if [[ "$DOMAIN" == "dev" ]]
then
  echo "Running tests.."
  python manage.py test social_app.tests
  echo "Starting server.."
  python manage.py runserver 0.0.0.0:8000
else
  gunicorn reunion.wsgi:application --bind :8000
fi
