#!/bin/bash
set -e

echo "🚀 Waiting for database to be ready..."

# Optional: a simple wait loop to ensure Postgres is reachable
until alembic upgrade head; do
  echo "❌ Alembic migration failed. Retrying in 5 seconds..."
  sleep 5
done

echo "✅ Migrations complete. Starting FastAPI server..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000