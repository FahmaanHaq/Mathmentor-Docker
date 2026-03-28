#!/bin/sh
set -e

# Wait for Postgres to be ready
echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        dbname=os.environ.get('DB_NAME', 'mathmentor'),
        user=os.environ.get('DB_USER', 'mathmentor'),
        password=os.environ.get('DB_PASSWORD', ''),
        host=os.environ.get('DB_HOST', 'db'),
        port=os.environ.get('DB_PORT', '5432'),
    )
    sys.exit(0)
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(1)
"; do
    echo "PostgreSQL unavailable – retrying in 2s..."
    sleep 2
done
echo "PostgreSQL is up."

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Daphne (ASGI server for Django Channels / WebSockets)
echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p 8000 mathmentor.asgi:application
