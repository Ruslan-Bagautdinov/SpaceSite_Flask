#!/bin/bash

until mysqladmin ping -h db -u root -p$MYSQL_PASSWORD --silent; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready!"

alembic upgrade head

flask run --host=0.0.0.0
