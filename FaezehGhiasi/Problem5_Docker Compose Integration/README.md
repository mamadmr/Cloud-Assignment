# Problem 5: Docker Compose Integration

This stage integrates all components of the CTF challenge management system into a single Docker Compose setup.

## Services

- **PostgreSQL (db)**: Stores challenge assignment data.
- **Redis (redis)**: Message broker for Celery tasks.
- **FastAPI Server (api)**: Provides endpoints to assign and remove challenges.
- **Celery Worker (worker)**: Executes container management tasks in the background.
- **Adminer (adminer)**: Web UI for managing the PostgreSQL database.
- **RedisInsight (redisinsight)**: Web UI for monitoring Redis.

## How to Use

To build and start the complete system, run:

```bash
docker compose up --build
```

Once running:

- FastAPI API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Adminer UI: [http://localhost:8080](http://localhost:8080)
- RedisInsight: [http://localhost:5540](http://localhost:5540)

## Project Highlights

- FastAPI endpoints (`/assign_challenge`, `/remove_challenge`) interact with Redis and PostgreSQL.
- Celery asynchronously handles starting and stopping Docker containers.
- Adminer and RedisInsight provide GUI tools for DB and Redis monitoring.
- The Docker socket is mounted inside the worker container to allow container control.
- Persistent volumes ensure PostgreSQL data is not lost on container restarts.

## Requirements

- Docker must be installed.
- Docker Compose must be installed.
- Ports 8000, 5432, 6379, 8080, and 5540 must be available.

## Notes

- FastAPI handles API requests quickly by delegating heavy work to Celery tasks.
- PostgreSQL manages active assignment tracking.
- Redis channels and task results are visible in RedisInsight.
- All services are isolated in a shared network for internal communication.

This completes the full system integration for CTF challenge container management!


