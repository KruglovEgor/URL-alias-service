#!/bin/sh
cd /app
export PYTHONPATH=/app
python -m app.db.init_db
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 