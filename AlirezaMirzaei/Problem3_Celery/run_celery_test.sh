#!/bin/bash

echo "Running Celery container management test..."
cd $(dirname "$0")

# Set Python path to include current directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Default values
CHALLENGE=${1:-"todo-app"}
TEAM_ID=${2:-"team1"}

# Run the test script
python test_celery_tasks.py $CHALLENGE $TEAM_ID

echo "Test completed!"
