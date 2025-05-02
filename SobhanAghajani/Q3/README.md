# Question 3

## Set Up Celery with Redis Broker

### Create a file celery_app.py
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')
```

### Implement Celery Tasks for Docker Control

####  Create a file tasks.py
```python
import docker
from celery_app import app

client = docker.from_env()


@app.task
def start_container(image_name, container_name=None):
    try:
        container = client.containers.run(
            image_name,
            name=container_name,
            detach=True
        )
        return f"Started container: {container.id}"
    except Exception as e:
        return f"Error starting container: {str(e)}"


@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Stopped container: {container_id}"
    except Exception as e:
        return f"Error stopping container: {str(e)}"

```

## Run and Demonstrate Celery

### Start Redis
```docker
docker run --name redis_container -p 6379:6379 -d redis 
```
### create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install docker redis celery
```
### Start the Celery worker
```docker
celery -A tasks worker --loglevel=info 
```
### Run start.py 
```python
python start.py pasapples/apjctf-todo-java-app:latest my_ctf_container
```
### Run stop.py
```python
python stop.py container_id
```