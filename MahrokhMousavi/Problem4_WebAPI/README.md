# CTF Challenge Management Web API

A Django-based web API to manage CTF challenge containers for multiple teams. Integrates Docker, Celery (with Redis), and a PostgreSQL database backend for scalable and asynchronous challenge lifecycle control.

---

## 📘 Table of Contents
- [Purpose of Endpoints](#purpose-of-endpoints)
- [Database Schema](#database-schema)
- [Celery and Redis Configuration](#celery-and-redis-configuration)
- [Key Code Components](#key-code-components)
- [Dockerfile Overview](#dockerfile-overview)
- [Setup & Run Instructions](#setup--run-instructions)
- [API Testing via Postman](#api-testing-via-postman)
- [Video Demonstration](#video-demonstration)

---

## 🔗 Purpose of Endpoints

| Endpoint            | Method | Description                                                                 |
|---------------------|--------|-----------------------------------------------------------------------------|
| `/api/assign/`      | POST   | Assign a CTF container to a team. Requires `team_id` and `challenge_id`.   |
| `/api/remove/`      | DELETE | Remove a container assignment. Requires `team_id` and `challenge_id`.      |
| `/api/list/`        | GET    | List all active container assignments with container access URLs.          |

---

## 🗃️ Database Schema

- **Team**: `id`, `team_id`, `name`
- **Challenge**: `id`, `challenge_id`, `name`, `image` (e.g., `bkimminich/juice-shop`)
- **Container**:
  - `id`
  - `team_id` → foreign key
  - `challenge_id` → foreign key
  - `container_id` → Docker container ID
  - `address` → e.g., `http://localhost:14528`
  - `created_at`

---

## ⚙️ Celery and Redis Configuration

- **Celery** uses:
  ```python
  broker = "redis://172.18.0.3:6379/0"
  result_backend = "redis://172.18.0.3:6379/0"
  ```

- **Redis** is a lightweight message broker for asynchronous task queuing.

---

## 🧩 Key Code Components

<details>
<summary><strong>Celery Tasks (challenges/tasks.py)</strong></summary>

### ✅ start_container_task(team_id, challenge_id)

- Connects to Docker using:
  ```python
  docker.DockerClient(base_url="unix:///var/run/docker.sock")
  ```
- Starts a container on `ctf_network`, dynamically assigns a port.
- **Port Resolution**: Initially, the task failed to capture the host port due to timing issues with Docker’s port mapping. This was fixed by implementing a retry mechanism with `container.reload()` to fetch updated port data, ensuring the correct host port (e.g., `14528`) is used in the `address` field instead of the container’s internal port (e.g., `3000`).
- Saves container info to DB and returns:
  ```json
  {
    "status": "success",
    "container_id": "abc123",
    "address": "http://localhost:14528"
  }
  ```

### 🛑 stop_container_task(container_id)

- Stops and removes the container.
- Deletes DB entry for the container.

</details>

---

## 🐳 Dockerfile Overview

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

- No `CMD` specified to support flexible entrypoints: Django server or Celery worker.

---

## 🚀 Setup & Run Instructions

### Prerequisites
- Docker installed
- Python 3.9
- Postman or curl

### Step-by-Step

```bash
# 1. Build API image
docker build -t ctf_api .

# 2. Start PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_USER=ctf_user \
  -e POSTGRES_PASSWORD=ctf_password \
  -e POSTGRES_DB=ctf_db \
  -p 5432:5432 \
  --network ctf_network \
  postgres

# 3. Start Redis
docker run -d --name redis -p 6379:6379 --network ctf_network redis

# 4. Start API server
docker run -d --name ctf_api \
  -p 8000:8000 \
  --network ctf_network \
  -e DJANGO_SETTINGS_MODULE=ctf_api.settings \
  ctf_api

# 5. Apply database migrations
docker exec ctf_api python manage.py makemigrations
docker exec ctf_api python manage.py migrate

# 6. Start Celery worker
docker run -d --name ctf_celery \
  -v //var/run/docker.sock:/var/run/docker.sock \
  --network ctf_network \
  -e DJANGO_SETTINGS_MODULE=ctf_api.settings \
  ctf_api \
  celery -A ctf_api worker --loglevel=info

# 7. Verify running containers
docker ps
```

### Database Management
- **Check Database Content**:
  ```bash
  docker exec -it ctf_api python manage.py shell
  ```
  In the shell:
  ```python
  from challenges.models import Team, Challenge, Container
  print(Team.objects.all())
  print(Challenge.objects.all())
  print(Container.objects.all())
  exit()
  ```
- **Fill the Database** (e.g., using Django shell or migrations):
  ```bash
  docker exec -it ctf_api python manage.py shell
  ```
  In the shell:
  ```python
  from challenges.models import Team, Challenge
  Team.objects.create(team_id="team1", name="Team1")
  Team.objects.create(team_id="team2", name="Team2")
  Challenge.objects.create(challenge_id="todo", name="Todo App", image="jetty:9.4-jre11-slim", port=8080)
  Challenge.objects.create(challenge_id="juice", name="Juice Shop", image="bkimminich/juice-shop", port=3000)
  exit()
  ```
  Alternatively, use a Django data migration for persistence.

---

## 📬 API Testing via Postman

### Assign a container
#### Test Case 1: Team2 - Juice Shop
```json
POST /api/assign/
{
  "team_id": "team2",
  "challenge_id": "juice"
}
```

#### Test Case 2: Team1 - Todo App
```json
POST /api/assign/
{
  "team_id": "team1",
  "challenge_id": "todo"
}
```

### Remove a container
```json
DELETE /api/remove/
{
  "team_id": "team2",
  "challenge_id": "juice"
}
```

### List all containers
```
GET /api/list/
```

---

## 🎥 Video Demonstration

📎 [Click here to view the video](https://iutbox.iut.ac.ir/)

> Shows:
>
> * API interaction via Postman
> * Containers starting/stopping in `docker ps`
> * Celery logs showing task execution
> * Database records updating

---

## Notes

- Ensure the Docker socket `//var/run/docker.sock` is accessible.
- Use Django Admin or fixtures to preload team/challenge data.
- Adjust container ports or images as per your actual challenge setup.
- Configure `DJANGO_SETTINGS_MODULE=ctf_api.settings` in your environment or settings file to connect to PostgreSQL.

---
