#!/bin/bash
set -e

echo "Running Alembic migrations..."
uv run alembic upgrade head

echo "Starting Litestar app..."
exec uvicorn app:app --host 0.0.0.0 --port 8000
