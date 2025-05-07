
# Problem 3: Container Management with Celery and Redis

## 📌 Description

This part of the assignment demonstrates how to:

- Use **Celery** and **Redis** to manage Docker containers in the background.
- Run asynchronous tasks that start and stop containers for CTF challenges.
- Observe container lifecycle changes (created → running → removed).
- Handle existing containers and error conditions gracefully.

Redis acts as the message broker and result backend for Celery, while Docker is managed via Python's Docker SDK.

---

## 🛠️ (a) Set Up Celery with Redis

### 1. Install Required Packages
```bash
pip install celery redis docker
````

### 2. Start a Redis Server

```bash
docker run -d --name my_redis -p 6379:6379 redis
```

---

## ⚙️ (b) Define Celery Tasks for Docker Management

📄 `tasks.py`

```python
from celery import Celery
import docker

app = Celery('ctf_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
client = docker.from_env()

@app.task
def start_ctf_container(image_name, container_name):
    try:
        try:
            existing = client.containers.get(container_name)
            if existing.status == 'running':
                return f"Container {container_name} already running"
            existing.remove()
        except docker.errors.NotFound:
            pass
        
        container = client.containers.run(image_name, name=container_name, detach=True)
        return f"Started container: {container.id}"
    except Exception as e:
        return f"Error starting container: {str(e)}"

@app.task
def stop_ctf_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return f"Stopped and removed container: {container_id}"
    except docker.errors.NotFound:
        return f"Container {container_id} not found"
    except Exception as e:
        return f"Error stopping container: {str(e)}"
```

---

## ▶️ (c) Run and Demonstrate the Tasks

📄 `main.py`

```python
from tasks import start_ctf_container, stop_ctf_container
import docker
import time

def manage_container(image_name="alpine", container_name="ctf-challenge"):
    client = docker.from_env()
    
    try:
        container = client.containers.get(container_name)
        print(f"Initial state: {container.status}")
    except:
        print("Initial state: No container")

    print("\nStarting container...")
    result = start_ctf_container.delay(image_name, container_name)
    while not result.ready():
        time.sleep(1)
    print(result.get())

    try:
        container = client.containers.get(container_name)
        print(f"State after start: {container.status}")
        container_id = container.id
    except:
        print("Failed to start container")
        return

    print("\nStopping container...")
    result = stop_ctf_container.delay(container_id)
    while not result.ready():
        time.sleep(1)
    print(result.get())

    try:
        container = client.containers.get(container_name)
        print(f"State after stop: {container.status}")
    except:
        print("State after stop: Removed")

if __name__ == "__main__":
    manage_container()
```

---

### 4. Start the Celery Worker

```bash
celery -A tasks worker --loglevel=info
```

---

## ⚠️ Windows Users (Python 3.12+)

If you're using **Windows with Python 3.12 or later**, Celery may crash with an error like:

```
ValueError: not enough values to unpack (expected 3, got 0)
```

### ✅ Fix:

Use the `solo` pool to avoid multiprocessing issues:

```bash
celery -A tasks worker --loglevel=info --pool=solo
```

This runs Celery tasks in the main process — perfectly fine for development.

---

## 🧪 Verify Docker Container State

You can observe changes before and after each task using:

```bash
docker ps -a
```

---

## 🖼️ Screenshots

### 🔹 Initial State (Before Starting Task)

> ![Initial Docker State](https://your-upload-link.com/before.png)

### 🔹 Celery Worker Output During Task Execution

> ![Celery Logs](https://your-upload-link.com/logs.png)

### 🔹 Final State (After Stopping Container)

> ![Final Docker State](https://your-upload-link.com/after.png)

Replace the links above with your real screenshot URLs.

---

## 💡 Reasoning Behind Decisions

* **Named containers (`ctf-challenge`)**: Reusable across tasks, avoids duplication.
* **Docker SDK for Python**: Enables full control of containers programmatically.
* **Redis as broker/backend**: Simplifies asynchronous task dispatch and result tracking.
* **Error handling**: Avoids crashes when containers already exist or don’t exist.

---

## 🎥 Demonstration Video

📎 [Click here to view the video](https://iutbox.iut.ac.ir/your-video-link)

> Should show:
>
> * Running `main.py`
> * Celery logs
> * `docker ps -a` before and after
> * Confirmation that container was started, stopped, and removed

---

