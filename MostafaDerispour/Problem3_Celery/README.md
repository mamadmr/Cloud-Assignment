# Command Explanations

This project uses a Python virtual environment and Celery to run background tasks. Follow the steps below to get everything up and running.

---

## Step 1: Set Up the Python Virtual Environment

Create a virtual environment named `env`:

```bash
python3 -m venv env
```

Activate the virtual environment:

```bash
source env/bin/activate
```

---

## Step 2: Install Python Dependencies

Install the required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Step 3: Run the Task Demo Script

This project includes a helper bash script (`run_ctf_demo.sh`) that does the following:

1. Stops and removes a Docker container named `ctf_test` (if it exists).
2. Activates the virtual environment.
3. Starts a Celery worker in the background and saves its PID.
4. Waits a few seconds to ensure the worker is ready.
5. Runs a Python script that triggers tasks.
6. Stops the Celery worker.

Here is the script:

```bash
#!/bin/bash

# Step 1: Remove old Docker container (if exists)
sudo docker rm -f ctf_test

# Step 2: Activate virtual environment
echo ">>> Activating virtual environment..."
source env/bin/activate

# Step 3: Start Celery worker in the background
echo ">>> Starting Celery Worker..."
celery -A tasks worker --loglevel=info > celery.log 2>&1 &
CELERY_PID=$!

# Step 4: Wait a bit to make sure Celery is ready
sleep 5

# Step 5: Run the Python script to call tasks
echo ">>> Running Python demo script..."
python3 run_tasks.py

# Step 6: Stop Celery worker
echo ">>> Stopping Celery Worker..."
kill $CELERY_PID
```

---

---
# Videos Link
https://iutbox.iut.ac.ir/index.php/s/RpzHAzQbQcokCBL
