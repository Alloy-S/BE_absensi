#!/bin/sh

echo "Running database migrations..."
flask db upgrade

echo "Starting Gunicorn..."
exec "$@"