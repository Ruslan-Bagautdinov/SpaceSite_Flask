#!/bin/sh

wait_for_db() {
    echo "Waiting for database..."
    while ! mysqladmin ping -h db --silent; do
        sleep 1
    done
    echo "Database is ready!"
}

wait_for_db

alembic upgrade head

flask run --host=0.0.0.0
