# Problem 3: Container Management with Celery and Redis

## Setup and Dependencies
Install the required Python libraries in virtual env:
```bash
pip install celery redis docker
```
---

## a) Set Up Celery with Redis as the Message Broker

### Step 1: Configuration
Celery was configured to use Redis as both the message broker and result backend in `tasks.py`:

```python
from celery import Celery

app = Celery(
    'ctf_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
```

---

### Step 2: Running Celery Worker
Start the Celery worker in a terminal :

```bash
celery -A tasks worker --loglevel=info
```

---

## b) Implement Celery Tasks for Container Management

### Step 1: Task Implementation
Two Celery tasks were defined in `tasks.py` :

```python
import docker
from celery.exceptions import SoftTimeLimitExceeded

docker_client = docker.from_env()

@app.task(bind=True, soft_time_limit=30, time_limit=40)
def start_container(self, image_name, container_name):
    try:
        try:
            existing_container = docker_client.containers.get(container_name)
            if existing_container.status == 'running':
                return f"Container {container_name} is already running."
            else:
                existing_container.start()
                return f"Container {container_name} started."
        except docker.errors.NotFound:
            container = docker_client.containers.run(
                image_name,
                name=container_name,
                detach=True
            )
            return f"Container {container_name} created and started with ID {container.id}."
    except SoftTimeLimitExceeded:
        return f"Task to start {container_name} timed out."
    except Exception as e:
        return f"Error starting container {container_name}: {str(e)}"

@app.task(bind=True, soft_time_limit=30, time_limit=40)
def stop_container(self, container_name):
    try:
        container = docker_client.containers.get(container_name)
        container.stop()
        return f"Container {container_name} stopped."
    except docker.errors.NotFound:
        return f"Container {container_name} not found."
    except SoftTimeLimitExceeded:
        return f"Task to stop {container_name} timed out."
    except Exception as e:
        return f"Error stopping container {container_name}: {str(e)}"
```

### Step 2: Testing Tasks

Create `test_tasks.py`:
```python
from tasks import start_container, stop_container
from time import sleep

result_start = start_container.delay('hello-world:latest', 'ctf-hello-world')
print(result_start.get(timeout=60))

time_to_sleep = 5
print(f"wait for {time_to_sleep} seconds")
sleep(time_to_sleep)

result_stop = stop_container.delay('ctf-hello-world')
print(result_stop.get(timeout=60))
```

---

## c) Demonstrate Task Execution and Container Lifecycle Management

### Step 1: main Example
```python
from tasks import start_container, stop_container
from time import sleep
import os

print("

Starting container...
")
result_start = start_container.delay('hello-world:latest', 'ctf-hello-world')
print(result_start.get(timeout=60))

os.system("docker ps")

time_to_sleep = 5
print(f"
wait for {time_to_sleep} seconds
")
sleep(time_to_sleep)

print("

Stopping container...
")
os.system("docker ps")

result_stop = stop_container.delay('ctf-hello-world')
print(result_stop.get(timeout=60))
```

