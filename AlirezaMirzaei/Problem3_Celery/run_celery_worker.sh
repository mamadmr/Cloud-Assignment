#!/bin/bash

echo "Starting Celery worker..."
cd $(dirname "$0")

# Set Python path to include current directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start the Celery worker
celery -A celery_app.celery_app worker --loglevel=info
