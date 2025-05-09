
---

## Setup Overview

**Running Redis inside a Docker container:**

```
docker run -d --name redis-broker -p 6379:6379 redis
```

This command runs Redis in a background container and exposes it on port 6379.

---

## Celery Configuration

The Celery application is configured in `celery_app.py` as follows:

* A Celery instance named `container_tasks` is created.
* Redis is used as both the message broker and result backend.
* Tasks are serialized in JSON.
* UTC is enabled for consistent task timing.

Example setup:

```python
from celery import Celery

app = Celery('container_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)
```

---

## Tasks Overview

Tasks are defined in `tasks.py` using the Docker SDK for Python.

**start\_container(image\_name, container\_name=None)**

* Starts a Docker container using a specified image.
* Runs in detached mode.
* Handles errors like missing images or naming conflicts.

**stop\_container(container\_id\_or\_name)**

* Stops a running Docker container by ID or name.
* Gracefully handles errors like non-existent or already stopped containers.

The Docker client is initialized using:

```python
import docker
client = docker.from_env()
```

---

## Running the Project

1. Start the Redis container:

```
docker run -d --name redis-broker -p 6379:6379 redis
```

2. Start the Celery worker:

```
celery -A tasks worker --loglevel=info
```

3. Run the test script to start and stop containers:

```
python test.py
```

This script uses `.delay()` to queue the tasks asynchronously.

---

## Verifying Task Execution

Check container status using:

```
docker ps -a      # View all containers (including stopped ones)
docker ps         # View only running containers
```

