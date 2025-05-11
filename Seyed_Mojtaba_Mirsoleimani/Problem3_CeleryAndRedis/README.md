# Container Management with Celery & Redis

> This project shows how to:
> 1. Use Redis as a message broker for Celery.  
> 2. Define Celery tasks to start and stop Docker containers asynchronously.  
> 3. Demonstrate task execution and container lifecycle management.  
> 4. Document your setup and record a short demo video.

---

## Table of Contents

- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Project Structure](#project-structure)  
- [Running the Celery Worker](#running-the-celery-worker)  
- [Demonstration Script](#demonstration-script)  
- [Verifying Task Execution](#verifying-task-execution)  
- [Recording a Demo Video](#recording-a-demo-video)  
- [License](#license)  

---

## Prerequisites

- Docker (version 20.10 or later)  
- Redis server running on `localhost:6379`  
- Python 3.8+  
- `pip` package manager  

---

## Installation

1. Clone this repository and enter its folder:
   ```bash
   git clone https://github.com/yourusername/ctf-container-tasks.git
   cd ctf-container-tasks

---

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Python dependencies:

   ```bash
   pip install celery redis docker
   ```

---

## Configuration

* **Redis Broker & Backend**
  Celery is configured to use Redis as both the broker (database 0) and result backend (database 1).
* **Docker Client**
  The tasks use the local Docker daemon via `docker.from_env()`. Make sure your user has permission to run Docker commands.

---

## Project Structure

```
.
├── celery_app.py       # Celery application definition
├── tasks.py            # start/stop container tasks
├── utilis.py           # demo script to invoke tasks
└── README.md
```

* **celery\_app.py**

  ```python
  from celery import Celery

  app = Celery(
      'docker_tasks',
      broker='redis://localhost:6379/0',
      backend='redis://localhost:6379/1'
  )
  ```
* **tasks.py**

  ```python
  import docker
  from celery_app import app

  client = docker.from_env()

  @app.task
  def start_container(image_name, ports=None):
      container = client.containers.run(image_name, detach=True, ports=ports)
      return container.id

  @app.task
  def stop_container(container_id):
      container = client.containers.get(container_id)
      container.stop()
      return f"Container {container_id} stopped"
  ```
* **utilis.py**

  ```python
  from tasks import start_container, stop_container
  import time

  print("Waiting for container to start…")
  result = start_container.delay("nginx:alpine", ports={"8080/tcp": 8080})
  container_id = result.get(timeout=20)
  print("Started container:", container_id)

  time.sleep(5)

  print("Stopping container…")
  stop_result = stop_container.delay(container_id)
  print(stop_result.get(timeout=20))
  ```

---

## Running the Celery Worker

In one terminal, launch the Celery worker so it can pick up your tasks:

```bash
python3 -m celery \
  -A celery_app worker \
  --loglevel=info \
  --include=tasks
```

You should see log lines indicating the worker is online and ready.

---

## Demonstration Script

In another terminal (with the worker still running), execute:

```bash
python3 utilis.py
```

This script will:

1. Submit the `start_container` task to pull and run `nginx:alpine` on host port 8080.
2. Wait for the container ID result.
3. Sleep 5 seconds.
4. Submit the `stop_container` task and print its result.

---

## Verifying Task Execution

* **Celery Worker Logs**
  You will see entries like:

  ```
  [tasks.py: start_container] Task received…
  [tasks.py: stop_container] Task succeeded…
  ```
* **Docker Containers**

  ```bash
  # List running containers before stopping:
  docker ps

  # After the script finishes, verify the container has stopped:
  docker ps -a
  ```

---

## License

This project is licensed under the MIT License.
Feel free to open issues or submit pull requests for enhancements.

```
```
