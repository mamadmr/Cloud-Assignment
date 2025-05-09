# Problem 3: Asynchronous Docker Container Management with Celery

## Project Structure

```
Problem3_Celery/
├── docker-compose.yml     # Defines Redis & worker services
└── worker/
    ├── Dockerfile         # Builds the Celery worker image
    └── tasks.py           # Contains start_ctf and stop_ctf task functions
```

---

## 1. Docker Compose Setup

Create `docker-compose.yml` in `Problem3_Celery/`:

```yaml
services:
  redis:
    image: redis:7            # Official Redis v7 image from Docker Hub
    container_name: ctf_redis # Friendly name for the container
    ports:
      - "6379:6379"           # Map host port 6379 → container port 6379
    volumes:
      - redisdata:/data       # Persist Redis data in a named volume

  worker:
    build: ./worker           # Build image from the Dockerfile in ./worker
    container_name: ctf_worker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - redis                 # Ensure Redis starts before worker

volumes:
  redisdata:                  # Named volume to persist Redis data
```

Explanation of fields:

- version: Chooses the Compose schema.
- services: Defines separate containers.
- image: Docker image to pull for a service.
- build: Directory containing a Dockerfile to build a custom image.
- container_name: Human-friendly name for easy docker ps lookup.
- ports: Host↔Container port mapping (host:container).
- volumes: Host path or named volume → Container path.
- depends_on: Orchestrates start order; worker waits until Redis is running.
- volumes (top-level): Defines named volumes for persistent storage.

---

## 2. Build & Launch

From the Q3/ directory, run:

```bash
docker-compose up --build -d
```

- --build: Rebuilds images if Dockerfiles changed
- -d: Runs containers in detached (background) mode

Verify both services:

```bash
docker ps --filter name=ctf_
```

You should see ctf_redis and ctf_worker up and running.

---

## 3. Dockerfile for the Worker

Create worker/Dockerfile:

```dockerfile
FROM python:3.10-slim

RUN pip install celery docker redis

WORKDIR /app

COPY tasks.py /app/tasks.py

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
```

Explanation:

1. FROM python:3.10-slim: Minimal Python base image.
2. RUN pip install...: Installs celery, Docker SDK, and redis client.
3. WORKDIR /app: Sets working directory inside the container.
4. COPY tasks.py...: Adds task definitions.
5. CMD [...]: Starts the Celery worker on container start.

---

## 4. Task Definitions (worker/tasks.py)

```python
from celery import Celery
import docker

app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1'
)

docker_client = docker.from_env()

@app.task(bind=True)
def start_ctf(self, image_name: str, team_id: str) -> str:
    try:
        name = f"{team_id}-{image_name}"
        try:
            existing = docker_client.containers.get(name)
            existing.stop()
            existing.remove()
        except docker.errors.NotFound:
            pass

        container = docker_client.containers.run(
            image_name,
            detach=True,
            name=name
        )
        return container.id
    except Exception as e:
        print("Error in start_ctf:", e)
        return None

@app.task(bind=True)
def stop_ctf(self, container_id: str) -> bool:
    try:
        container = docker_client.containers.get(container_id)
        container.stop()
        container.remove()
        print(f"Container {container_id} stopped and removed.")
        return True
    except Exception as e:
        print(f"Unexpected error in stop_ctf: {e}")
        return False

```

---

## 5. Running Tasks from CLI

Start a container:

```bash
celery -A tasks call tasks.start_ctf --args '["pasapples/apjctf-todo-java-app:latest","team1"]'
```
- pasapples/apjctf-todo-java-app:latest : Image Name 
- team1 : Container Name

Verify running:

```bash
docker ps --filter name=team1-pasapples/apjctf-todo-java-app:latest
```

Stop & remove container:

```bash
celery -A tasks call tasks.stop_ctf --args '["<container_id>"]'
```

---

## 6. Logs & Debugging

```bash
docker-compose logs -f worker
docker ps -a
docker logs team42-nginx
```
---
🎥 [Watch the video](https://iutbox.iut.ac.ir/index.php/s/G3WKBDLfL8d22j7)