# Problem 3: Celery and Docker Container Management

This project sets up an asynchronous container management system using Celery, Redis, and Docker. It allows starting and stopping Docker containers through background tasks managed by Celery workers.

## Services

- **Redis**: A message broker for Celery tasks.
- **Celery Worker**: A background worker that processes tasks like starting and stopping containers.
- **Test Runner**: A one-time service that sends test tasks to Celery for execution.

## How to Use

To start all the services, open your terminal in the project directory and run:

```bash
docker compose up --build
```

This will build and start:
- Redis server
- Celery worker
- Test runner script (which will create and remove a Docker container)

## Project Files

- **celery_app.py**: Configures Celery to use Redis as the broker and backend.
- **tasks.py**: Defines two Celery tasks:
  - `start_container`: Start a Docker container with a given image and name.
  - `stop_container`: Stop and remove a Docker container by name.
- **test_tasks.py**: Sends a task to start a container and then a task to stop and remove it.
- **docker-compose.yml**: Defines services and their relationships.
- **Dockerfile.worker**: Dockerfile for building the Celery worker image.
- **Dockerfile.test**: Dockerfile for building the test runner image.
- **requirements.txt**: Python dependencies for the project.


## Requirements

- Docker must be installed.
- Docker Compose must be installed.
- Python 3 must be installed (for running test scripts manually).
- Docker daemon must be running.


## Notes

- The Docker socket `/var/run/docker.sock` is mounted into the worker and test runner containers to allow Docker SDK to interact with the host's Docker engine.
- The Celery tasks run asynchronously in the background and communicate through Redis.
- Containers are named consistently to avoid conflicts during start/stop operations.




