#!/bin/bash
set -e

echo "Running Alembic migrations..."
uv run alembic upgrade head

echo "Starting Litestar app..."
uvicorn main:app --host 0.0.0.0 --port 8000 \
    --log-level debug \
    --log-config log.ini
