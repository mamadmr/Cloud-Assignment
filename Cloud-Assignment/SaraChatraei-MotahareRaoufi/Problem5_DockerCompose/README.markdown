# My Docker Compose Integration for CTF Challenge Management API

For my assignment, I integrated my Web API for managing Capture The Flag (CTF) challenge containers into a Docker Compose setup. This report explains how I created a `docker-compose.yml` file to orchestrate all services, ensured they work together, and set up persistent data storage. I also describe how the services are connected, provide instructions to start and use the system, and outline my plan for a demonstration video. This builds on my previous work with the FastAPI-based API, PostgreSQL database, Celery, Redis, and Docker container management.

---

## Overview of My Docker Compose Setup

I created a Docker Compose setup to run all components of my CTF challenge management system in a cohesive environment. The system includes:

- **PostgreSQL**: Stores assignment data in a database.
- **Redis**: Acts as the message broker and result backend for Celery.
- **Celery Worker**: Handles asynchronous tasks for starting and stopping Docker containers.
- **Web API**: A FastAPI application that exposes endpoints to assign and remove containers.
- **CTF Challenge Containers**: Docker containers (using `python:3.12`) created dynamically for teams.

My Docker Compose setup ensures all services can communicate, uses volume mounts for persistent data, and starts seamlessly with a single command. I tested the system to confirm that I can assign and remove challenges using Postman, with all components working together.

---

## My `docker-compose.yml` File

I wrote a `docker-compose.yml` file to define and configure all services. Below is the file I created:

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: mot
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A tasks worker --loglevel=info
    depends_on:
      - redis
      - postgres
    volumes:
      - .:/app
      - /var/run/docker.sock:/var/run/docker.sock

  web:
    build: .
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    depends_on:
      - celery_worker
      - redis
      - postgres
    volumes:
      - .:/app
      - /var/run/docker.sock:/var/run/docker.sock

volumes:
  pgdata:
```

### Explanation of `docker-compose.yml`

- **Services**:
  - **postgres**: Runs PostgreSQL 15 with a user `mot`, password `mypassword`, and database `mydb`. I mapped port `5432` and used a volume `pgdata` for persistent storage.
  - **redis**: Runs Redis 7 and exposes port `6379` for Celery communication.
  - **celery_worker**: Builds from my `Dockerfile`, runs the Celery worker, and depends on `redis` and `postgres`. I mounted the project directory and Docker socket to allow container management.
  - **web**: Builds from my `Dockerfile`, runs the FastAPI server with Uvicorn, and exposes port `8000`. It depends on all other services and uses the same volume mounts.
- **Volumes**: I created a `pgdata` volume to ensure PostgreSQL data persists across container restarts.
- **Networking**: Docker Compose automatically creates a default bridge network, allowing all services to communicate using their service names (e.g., `postgres`, `redis`).

---

## How the Services Are Connected

I designed the services to work together seamlessly:

- **Web API and PostgreSQL**: My FastAPI application (`main.py`) connects to the PostgreSQL service using the connection string `postgresql://mot:mypassword@postgres:5432/mydb`. The service name `postgres` resolves to the container's IP within the Docker network.
- **Web API and Celery**: The API queues tasks (e.g., `start_container`, `stop_container`) using Celery, which communicates with the `redis` service as the message broker.
- **Celery and Redis**: The Celery worker (`celery_worker` service) uses Redis (`redis://redis:6379/0`) for task queuing and result storage. The service name `redis` resolves within the Docker network.
- **Celery and Docker**: The `celery_worker` and `web` services mount the Docker socket (`/var/run/docker.sock`) to interact with the Docker daemon on the host, allowing them to start and stop CTF challenge containers.
- **CTF Containers**: When I assign a challenge, Celery starts a `python:3.12` container, and its IP address is stored in the PostgreSQL database. These containers run on the default Docker network, accessible by their IP addresses.

The `depends_on` directives ensure that services start in the correct order: `postgres` and `redis` start first, followed by `celery_worker`, and finally `web`. The default Docker bridge network enables communication between all services.

---

## Starting and Using My System

### Prerequisites

- **Docker and Docker Compose**: I installed Docker and Docker Compose on my machine.
- **Project Files**:
  - `Dockerfile`: Builds the image for my `web` and `celery_worker` services.
  - `main.py`: My FastAPI application.
  - `tasks.py`: My Celery tasks for container management.
  - `docker-compose.yml`: Orchestrates all services.
  - `requirements.txt`: Lists Python dependencies (e.g., `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `celery`, `docker`).

### My `Dockerfile`

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- **Purpose**: Builds a Docker image for the `web` and `celery_worker` services.
- **Details**:
  - Uses `python:3.12` as the base image.
  - Sets `/app` as the working directory.
  - Installs dependencies from `requirements.txt`.
  - Copies my project files.
  - Specifies a default command for the `web` service (overridden for `celery_worker` in `docker-compose.yml`).

## Video report available at 