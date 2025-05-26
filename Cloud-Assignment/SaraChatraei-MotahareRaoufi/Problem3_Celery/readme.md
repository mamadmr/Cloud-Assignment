# Problem3: Celery

## 1. Setting Up Celery with Redis

To begin, I configured Celery to use Redis as the broker. I installed the necessary packages and ensured connectivity between Celery and Redis.
Dependencies Installed:

```bash
pip install celery redis docker
```

Directory Structure:

ctf_celery/
├── tasks.py
├── celeryconfig.py
└── __init__.py

### celeryconfig.py
``` python
broker_url = 'redis://localhost:6379/0'
```

### tasks.py
``` python
from celery import Celery
import docker
app = Celery('ctf_tasks')
app.config_from_object('celeryconfig')
client = docker.from_env()

@app.task
def start_container(image_name, container_name):
    try:
        container = client.containers.run(image_name, name=container_name, detach=True)
        return f"Container '{container_name}' started."
    except Exception as e:
        return f"Failed to start container '{container_name}': {str(e)}"

@app.task
def stop_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return f"Container '{container_name}' stopped and removed."
    except Exception as e:
        return f"Failed to stop container '{container_name}': {str(e)}"
```


## 2. Running the Celery Worker
To test the task system, I started the Redis server and then launched the Celery worker:

```bash
# Start Redis (if not already running)
docker run -d --name redis-server -p 6379:6379 redis

# Start Celery worker
celery -A tasks worker --loglevel=info
```

Celery connected successfully to Redis, and the worker began listening for tasks.



## 3. Triggering the Tasks

Using a simple Python script or a Python shell, I called the tasks to manage containers:

```python
from tasks import start_container, stop_container
# Start Juice Shop container
start_container.delay('bkimminich/juice-shop', 'juice_shop_ctf')
# Later, stop it
stop_container.delay('juice_shop_ctf')
```

These tasks executed in the background. I could observe their lifecycle using:

```bash
docker ps -a
```

Before calling start_container, the container wasn't listed. After execution, it appeared as running. Similarly, after calling stop_container, it was removed as expected.


## Video report available at https://iutbox.iut.ac.ir/index.php/s/DF8qNJGBydxb55B
