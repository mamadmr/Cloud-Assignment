#!/bin/bash

sudo docker rm -f ctf_test 

# Step 0: Activate virtual environment
echo ">>> Activating virtual environment..."
source env/bin/activate

# Step 2: Start Celery worker in the background
echo ">>> Starting Celery Worker..."
celery -A tasks worker --loglevel=info > celery.log 2>&1 &
CELERY_PID=$!

# Wait a bit to make sure Celery is ready
sleep 5

# Step 3: Run the Python script to call tasks
echo ">>> Running Python demo script..."
python3 run_tasks.py

# Step 4: Stop Celery worker
echo ">>> Stopping Celery Worker..."
kill $CELERY_PID
