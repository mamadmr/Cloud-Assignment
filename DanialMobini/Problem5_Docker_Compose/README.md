# Docker Compose System Explanation

This docker-compose.yml defines a system with four interconnected services:

## Services and Connections

1. **web** (CTF API):
   - Flask application running on port 8000
   - Connects to:
     - PostgreSQL database (`db`) using `DATABASE_URL`
     - Redis (`redis`) using `CELERY_BROKER_URL`
   - Has access to Docker socket (for container management)

2. **celery** (Worker):
   - Celery worker processing tasks from the "containers" queue
   - Shares the same codebase as web (same build)
   - Connects to same Redis and PostgreSQL as web

3. **redis**:
   - Message broker for Celery (task queue)
   - Exposes port 6379

4. **db** (PostgreSQL):
   - Database server with preconfigured database "ctfdb"
   - Credentials: admin/dani
   - Exposes port 5432

## How to Start and Use the System

1. **Starting the system**:

```bash
docker-compose up -d
```

2. **Accessing services**:
   - Web API: `http://localhost:8000`
   - PostgreSQL: `localhost:5432` (user: admin, password: dani, db: ctfdb)
   - Redis: `localhost:6379`

3. **System workflow**:
   - The web service (Flask) handles HTTP requests
   - Long-running tasks can be offloaded to Celery via Redis
   - Celery workers process tasks from the "containers" queue
   - Both web and celery services persist data to PostgreSQL

4. **Stopping the system**:

```bash
docker-compose down
```

**Assign a container:**

```bash
curl -X POST http://localhost:8000/assign-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "juice-shop"}'

curl -X POST http://localhost:8000/assign-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 2, "challenge_id": "nginx"}'
```

**Remove a container:**

```bash
curl -X DELETE http://localhost:8000/remove-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "juice-shop"}'

curl -X DELETE http://localhost:8000/remove-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 2, "challenge_id": "nginx"}'
```
