# Problem 4: Web API for Challenge Management

This project implements a Web API using FastAPI to manage CTF challenge container assignments for teams.
The API communicates with Redis and Celery to asynchronously start and stop containers, and stores challenge assignments in a PostgreSQL database.

## Services

- **FastAPI**: Web API server for managing challenge assignments.
- **PostgreSQL**: Database for storing assignment information.
- **Redis**: Message broker for Celery tasks.
- **Celery Worker**: Background worker to handle container start/stop operations.
- **Adminer**: Web UI for managing the PostgreSQL database.
- **RedisInsight**: Web UI for managing and monitoring Redis.

## Endpoints

- `POST /api/v1/assign_challenge`:
  - Assigns a challenge container to a team.
  - Launches a container using Celery task.

- `POST /api/v1/remove_challenge`:
  - Stops and removes the assigned container for a team.

## How to Use

1. Build and start all services:

```bash
docker compose up --build
```

2. Access services:

- API Documentation (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Adminer: [http://localhost:8080](http://localhost:8080)
- RedisInsight: [http://localhost:5540](http://localhost:5540)

3. Test API endpoints using Swagger UI or Postman.

## Requirements

- Docker must be installed.
- Docker Compose must be installed.
- Python 3 must be installed (for local development).
- Ports 8000, 5432, 6379, 8080, and 5540 must be available.

## Screenshots 📸
![Screenshot from 2025-05-02 01-22-56](https://github.com/user-attachments/assets/cdffbaa6-d40a-40b8-b247-9d9c5b00e824)
![Screenshot from 2025-05-02 01-23-26](https://github.com/user-attachments/assets/a3bba297-0044-487c-8df9-45fb5905c846)

## Notes

- Celery tasks are used to start and stop Docker containers asynchronously.
- PostgreSQL stores all active assignments with team and challenge information.
- Duplicate assignment requests are handled properly with HTTP conflict responses.
- BackgroundTasks are optionally used to further optimize API responsiveness.


