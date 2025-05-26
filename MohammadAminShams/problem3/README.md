# Problem 3: Container Management with Celery and Redis

## Setup and Dependencies

### Dependencies
Install the required Python libraries:
```bash
pip install celery redis docker
```
- `celery`: For running asynchronous tasks.
- `redis`: For connecting to the Redis message broker.
- `docker`: For interacting with the Docker API.

## Section (a): Set Up Celery with Redis as the Message Broker

### Configuration
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

### Running Celery Worker
Start the Celery worker in a terminal:
```bash
celery -A tasks worker --loglevel=info
```

**Example Output**:
```
[2025-05-05 16:21:32,941: INFO/MainProcess] Connected to redis://localhost:6379/0
[2025-05-05 16:21:32,943: INFO/MainProcess] mingle: searching for neighbors
[2025-05-05 16:21:33,949: INFO/MainProcess] mingle: all alone
[2025-05-05 16:21:33,986: INFO/MainProcess] celery@javad-ThinkBook-15-G2-ITL ready.
```

## Section (b): Implement Celery Tasks for Container Management

### Task Implementation
Two Celery tasks were defined in `tasks.py` to manage Docker containers:

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

### Testing Tasks

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

Run worker and script:
```bash
celery -A tasks worker --loglevel=info
python test_tasks.py
```

## Section (c): Demonstrate Task Execution and Container Lifecycle Management

### main.py Example
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

### Expected Output:
```
Starting container...
Container ctf-hello-world created and started with ID 4eca32584c2a.

... (docker ps output)

wait for 5 seconds

Stopping container...

... (docker ps output)

Container ctf-hello-world stopped.
```

### Summary
- Used Redis as broker.
- Celery task management with `docker-py`.
- Lifecycle control through `start_container` and `stop_container`.
- Demonstration via `main.py` and `docker ps`.
- Timeout, error handling included.
