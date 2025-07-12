This system manages CTF challenge containers using a Flask web API, asynchronous task processing with Celery, Docker container orchestration, PostgreSQL for persistence, and Redis as the message broker.

The components communicate over Docker Compose's default network and use Docker socket binding to allow Celery to control containers on the host.

Services and Docker Compose Configuration
The system is defined in a single docker-compose.yml file with the following services:

1. web
Build Context: The current directory (.) with the provided Dockerfile.

Purpose: Runs the Flask web API to handle HTTP requests to start and stop challenge containers.

Ports: Maps container port 5000 to host port 5000, so the API is accessible on http://localhost:5000.

Volumes: Mounts the current directory inside the container (.:/app) for live code changes.

Environment Variables:

FLASK_APP=app.py — Specifies the Flask app entrypoint.

FLASK_RUN_HOST=0.0.0.0 — Allows the Flask app to listen on all interfaces.

FLASK_RUN_PORT=5000 — Runs Flask on port 5000.

Dependencies: Starts after redis and db services are available.

2. redis
Image: Official Redis image (redis:latest).

Purpose: Provides the message broker service for Celery to queue tasks.

Ports: Exposes Redis default port 6379 to the host.

3. celery
Build Context: Same as web (the current directory).

Purpose: Runs the Celery worker that executes asynchronous container management tasks.

Command: Starts Celery worker with celery -A tasks worker --loglevel=info --pool=solo.

Volumes:

Mounts current directory for code access.

Mounts Docker socket (/var/run/docker.sock) to manage Docker containers on the host.

Dependencies: Starts after redis and db services.

4. db
Image: Official PostgreSQL image (postgres:15).

Purpose: Stores container metadata (team, challenge, container info).

Environment Variables:

POSTGRES_DB=ctfdb

POSTGRES_USER=postgres

POSTGRES_PASSWORD=1111

Volumes: Uses Docker volume pgdata to persist database data.

Ports: Maps PostgreSQL default port 5432 to host port 5432.

5. Volumes
pgdata: Docker volume to persist PostgreSQL data across container restarts.

How the Services Interact
The web service connects to the db to store and retrieve container info.

The web service sends tasks to redis, the message broker.

The celery worker consumes tasks from redis and interacts with Docker via the mounted Docker socket to start/stop containers.

The celery worker also updates the db to reflect container states.

All services communicate over the internal Docker network, using service names (db, redis) for connections.

How to Run and Use the System
Start all services:
In bash: docker-compose up --build
Access the API:
The Flask API listens on port 5000 of your host machine.

Start a challenge container:
In Postman:
POST http://localhost:5000/start
Content-Type: application/json

{
  "team_id": "team1",
  "challenge": "juice"
}
Stop a challenge container:
In Postman:
POST http://localhost:5000/stop
Content-Type: application/json

{
  "team_id": "team1",
  "challenge": "juice"
}
Celery will manage container lifecycle asynchronously, and PostgreSQL will keep metadata persistent.

