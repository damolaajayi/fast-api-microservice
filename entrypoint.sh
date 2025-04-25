# entrypoint.sh
#!/usr/bin/env bash
set -euo pipefail

echo "▶️  Running Alembic migrations …"
alembic upgrade head
echo "✅  Migrations complete"

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
