# CTF API Documentation

## Overview

This API provides functionality to manage teams, challenges, and Docker containers for a Capture The Flag (CTF) platform. It uses FastAPI as the web framework, PostgreSQL as the database, Celery with Redis for asynchronous task management, and Docker for container orchestration.

---

## API Endpoints

| Endpoint               | Method | Purpose                                                   | Sample Request Body                                                                                 |
|------------------------|--------|-----------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `/api/create-team/`     | POST   | Create a new team                                         | `{ "team_id": "team123", "team_name": "Team Alpha" }`                                            |
| `/api/create-challenge/`| POST   | Create a new challenge                                    | `{ "challenge_id": "challenge123", "name": "Challenge 1", "image": "challenge_image", "port": 80 }` |
| `/api/assign-container/`| POST   | Assign and start a container for a team and challenge    | `{ "team_id": "team123", "challenge_id": "challenge123" }`                                       |
| `/api/remove-container/`| DELETE | Stop and remove the container assigned to a team/challenge| `{ "team_id": "team123", "challenge_id": "challenge123" }`                                       |
| `/api/list-containers/` | GET    | List all running containers with assigned teams and challenges | No body                                                                                        |

---

## Database Schema

The database consists of three tables:

### teams

| Column    | Type    | Description           |
|-----------|---------|-----------------------|
| id        | Integer | Primary key           |
| team_id   | String  | Unique team identifier|
| team_name | String  | Team's name           |

### challenges

| Column       | Type    | Description           |
|--------------|---------|-----------------------|
| id           | Integer | Primary key           |
| challenge_id | String  | Unique challenge ID   |
| name         | String  | Challenge name        |
| image        | String  | Docker image name     |
| port         | Integer | Port exposed by challenge |

### containers

| Column       | Type      | Description                     |
|--------------|-----------|---------------------------------|
| id           | Integer   | Primary key                     |
| team_id      | String    | Team assigned to the container  |
| challenge_id | String    | Challenge assigned              |
| container_id | String    | Docker container ID             |
| address      | String    | URL to access the running container |
| created_at   | DateTime  | Timestamp when container was created |

---

## Celery and Redis Configuration

- **Broker and backend:** Redis is used for both message broker and result backend.
- Redis URL is read from `.env` file (`redis://localhost:6379/0`).
- Celery app is initialized as:

  ```python
  celery = Celery("ctf_tasks", broker=REDIS_URL, backend=REDIS_URL)
  ```

- Celery workers execute two main asynchronous tasks:
  - `start_container`: Runs a Docker container and stores its info in the database.
  - `stop_container`: Stops and removes a Docker container and deletes the record from the database.

---

## Setup and Run Instructions

### Prerequisites

- Docker installed and running
- PostgreSQL running (locally or in Docker)
- Redis running (locally or in Docker)
- Python 3.8+

### Steps

1. Clone the repository and navigate to the project directory.

2. Create a `.env` file with the following variables (adjust as needed):

    ```
    DATABASE_URL=postgresql://username:password@localhost:5432/ctf_db
    REDIS_URL=redis://localhost:6379/0
    ```

3. Ensure PostgreSQL and Redis services are running.

4. Run the FastAPI server with:

    ```bash
    uvicorn app.main:app --reload
    ```

5. Start the Celery worker in a separate terminal:

    ```bash
    celery -A app.celery_app worker --loglevel=info
    ```

---

## Example Usage via FastAPI Interactive Docs and Sample Payloads

### 1. Open API docs in your browser

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can see all API endpoints and interact with them directly through the Swagger UI.

### 2. Available API Endpoints

- `POST /api/create-team/`
- `POST /api/create-challenge/`
- `POST /api/assign-container/`
- `DELETE /api/remove-container/`
- `GET /api/list-containers/`

### 3. Sample JSON Payloads for Testing

### Create Team
```json
{
  "team_id": "team2",
  "team_name": "Red Dragons"
}
```
### Create Challenge
```
{
  "challenge_id": "challenge2",
  "name": "Ultimate Puzzle",
  "image": "nginx",
  "port": 8080
}
```
### Assign Container
```
{
  "team_id": "team2",
  "challenge_id": "challenge2"
}
```
### Remove Container
```
{
  "team_id": "team2",
  "challenge_id": "challenge2"
}
```
### List Containers

**GET** `/api/list-containers/`

Lists all currently running containers along with their assigned teams and challenges.

**Example using cURL:**

```bash
curl http://127.0.0.1:8000/api/list-containers/
```
---

## Video Demonstration

▶️ [CTF API Demo Video](https://iutbox.iut.ac.ir/index.php/s/3Wqz2Et5QjiS9fb)
