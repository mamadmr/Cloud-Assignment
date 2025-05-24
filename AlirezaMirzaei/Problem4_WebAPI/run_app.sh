#!/bin/bash

# Load env variables from .env if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Install dependencies
pip install -r requirements.txt

# Run database migrations (create tables)
python -c "from app.database import Base, engine; import app.models; Base.metadata.create_all(bind=engine)"

# Start celery worker in background
celery -A celery_app.celery_app worker --loglevel=info &

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000
