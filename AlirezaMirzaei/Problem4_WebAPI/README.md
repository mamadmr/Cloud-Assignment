## Problem 4: Web API for Team Challenge Management

### Overview

This service provides HTTP endpoints to assign and remove CTF challenge containers to/from teams. It uses:

- **FastAPI** for HTTP API
- **PostgreSQL** for persistent storage
- **Celery** with **Redis** for background task processing
- **Docker SDK** for container management

### Endpoints

#### `POST /assign`

Request:

```json
{
  "team_id": 1,
  "challenge_id": 2
}
```

Response:

```json
{
  "team_id": 1,
  "challenge_id": 2,
  "container_id": "...",
  "address": "http://<ip>:<port>",
  "status": "running"
}
```

#### `POST /remove`

Request:

```json
{
  "team_id": 1,
  "challenge_id": 2
}
```

Response:

```json
{
  "team_id": 1,
  "challenge_id": 2,
  "container_id": "...",
  "status": "stopped"
}
```

### Database Schema

Table: `team_challenges`

| Column         | Type    | Description                          |
| -------------- | ------- | ------------------------------------ |
| `id`           | Integer | Primary key                          |
| `team_id`      | Integer | ID of the team                       |
| `challenge_id` | Integer | ID of the challenge                  |
| `container_id` | String  | Docker container ID                  |
| `address`      | String  | URL address of the running container |
| `status`       | String  | `running` or `stopped`               |

### Setup and Run

1. Configure environment variables (copy from .env.example in project root) in a `.env` file:

```ini
DATABASE_URL=postgresql://postgres:password@postgres_ctf:5432/ctf_db
CELERY_BROKER_URL=redis://redis-server-ip:6379/0
...
```

#### Instead of the steps below, until the testing section, after running the redis and pgsql containers using .sh files given in the previous sections, you can run ./run_app.sh to do the steps 2 through 4

2. Build and install dependencies:

```bash
pip install -r requirements.txt
```

3. Start Celery worker:

```bash
celery -A celery_app.celery_app worker --loglevel=info
```

4. Run the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing with Postman or Python

Send a `POST` to `http://localhost:8000/assign` with JSON:

```json
{ "team_id": 1, "challenge_id": 2 }
```

Observe that a container starts, and the database record is created.

Send a `POST` to `http://localhost:8000/remove` with JSON:

```json
{ "team_id": 1, "challenge_id": 2 }
```

Observe the container stops and the record status updates.

You can also use `test_api.py` to quickly verify the endpoints using Python.

### End. The video links:

https://iutbox.iut.ac.ir/index.php/s/oLbwink98GPyA36
