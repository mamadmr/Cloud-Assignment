
# Q3 – CTF Container Management using Celery and Redis (Dockerized)

This project is part of a cloud computing assignment. It demonstrates how to use **Celery**, **Redis**, and **Docker SDK** to asynchronously start and stop CTF challenge containers using background workers.

---

## 📦 Technologies Used

- 🐳 Docker, Docker Compose
- 🐍 Python 3.11
- ⚙️ Celery (asynchronous task queue)
- 🧠 Redis (message broker and result backend)
- 🧰 Docker SDK (to manage containers programmatically)

---

## 🧱 Project Structure

```

q3/
├── config/
│   └── celery\_setup.py        ← Celery configuration
├── worker/
│   └── manager.py             ← Celery tasks (start/stop container)
├── runner/
│   └── launcher.py            ← Script that sends tasks to worker
├── Dockerfile.worker          ← Dockerfile for celery worker
├── Dockerfile.runner          ← Dockerfile for test task runner
├── docker-compose.yml         ← Compose file to orchestrate services
├── requirements.txt           ← Python dependencies
└── README.md

````

---

## 🚀 How to Run the Project

```bash
sudo docker compose up --build
````

The test launcher will:

1. Asynchronously start a Docker container using the worker
2. Then stop and remove it

---

## 📂 Code Explanations

### 📌 `Dockerfile.worker`

This file defines the container that runs the Celery worker:

```Dockerfile
FROM python:3.11-slim

WORKDIR /src
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "worker.manager", "worker", "--loglevel=info"]
```

**Explanation:**

* Uses a slim Python 3.11 base image
* Sets the working directory to `/src`
* Copies all source code into the container
* Installs Python dependencies
* Starts the Celery worker with the task module `worker.manager`

---

### 📌 `Dockerfile.runner`

This container runs a one-time script to test the start/stop tasks:

```Dockerfile
FROM python:3.11-slim

WORKDIR /src
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "runner/launcher.py"]
```

**Explanation:**

* Same base image and setup as the worker
* Instead of starting Celery, it runs the Python script `launcher.py` once to trigger tasks

---

### 📌 `docker-compose.yml`

This file orchestrates all the services:

```yaml
services:
  redis:
    image: redis
    ports:
      - "6379:6379"
    restart: always

  celery_worker:
    build:
      context: .
      dockerfile: Dockerfile.worker
    container_name: celery_worker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - redis
    restart: always

  test_launcher:
    build:
      context: .
      dockerfile: Dockerfile.runner
    container_name: test_launcher
    depends_on:
      - celery_worker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: "no"
```

**Explanation:**

* `redis`: the message broker for Celery
* `celery_worker`: runs background tasks to start/stop Docker containers
* `test_launcher`: sends a test task and exits after execution
* Docker socket is mounted so containers can control other containers

---

## 📌 Task Behavior

### `start_container` task:

* Takes a team name, challenge name, and image
* Builds a dynamic container name
* Starts a new container using the given image

### `stop_container` task:

* Stops and removes the given container by name

---

## ✅ Sample Output

```bash
Started: {'status': 'running', 'name': 'teamX_juice_173218', 'short_id': 'dae351429c94'}
Stopped: {'status': 'removed', 'name': 'teamX_juice_173218'}
```

---

## 🎥 Demo Suggestions

When recording your demo:

1. Run `docker compose up --build`
2. Show Redis and Celery connecting
3. Confirm the test container launches and completes
4. Show logs that the task succeeded
5. (Optional) Run `docker ps -a` to confirm containers were created and removed

---

