# 🚩 CTF Challenge Management Web API

A Django-based web API to manage CTF challenge containers for multiple teams. Integrates Docker, Celery (with Redis), and a database backend for scalable and asynchronous challenge lifecycle control.

---

## 📚 Table of Contents
- [🔗 Purpose of Endpoints](#-purpose-of-endpoints)
- [🗃️ Database Schema](#️-database-schema)
- [⚙️ Celery and Redis Configuration](#️-celery-and-redis-configuration)
- [🔧 Key Code Components](#-key-code-components)
- [🐳 Dockerfile Overview](#-dockerfile-overview)
- [🚀 Setup & Run Instructions](#-setup--run-instructions)
- [📺 Video Demonstration](#-video-demonstration)

---

## 🔗 Purpose of Endpoints

| Endpoint            | Method | Description                                                                 |
|---------------------|--------|-----------------------------------------------------------------------------|
| `/api/assign/`      | POST   | Assign a CTF container to a team. Requires `team_id` and `challenge_id`.   |
| `/api/remove/`      | DELETE | Remove a container assignment. Requires `team_id` and `challenge_id`.      |
| `/api/list/`        | GET    | List all active container assignments with container access URLs.          |

---

## 🗃️ Database Schema

- **Team**: `id`, `name`, ...
- **Challenge**: `id`, `challenge_id`, `image` (e.g., `bkimminich/juice-shop`)
- **Container**:
  - `id`
  - `team_id` → foreign key
  - `challenge_id` → foreign key
  - `container_id` → Docker container ID
  - `address` → e.g., `http://172.18.0.5:3000`

---

## ⚙️ Celery and Redis Configuration

- **Celery** uses:
  ```python
  broker = "redis://172.18.0.3:6379/0"
  result_backend = "redis://172.18.0.3:6379/0"
  ```

- **Redis** is a lightweight message broker for asynchronous task queuing.

---

## 🔧 Key Code Components

<details>
<summary><strong>Celery Tasks (challenges/tasks.py)</strong></summary>

### ✅ `start_container_task(team_id, challenge_id)`

- Connects to Docker using:
  ```python
  docker.DockerClient(base_url="unix:///var/run/docker.sock")
  ```
- Starts a container on `ctf_network`, dynamically assigns a port.
- Saves container info to DB and returns:
  ```json
  {
    "status": "success",
    "container_id": "abc123",
    "address": "http://172.18.0.5:3000"
  }
  ```

### 🛑 `stop_container_task(container_id)`

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

### ✅ Prerequisites
- Docker installed
- Python 3.9
- Postman or curl

### 🔨 Step-by-Step

```bash
# 1. Build API image
docker build -t ctf_api .

# 2. Start Redis
docker run -d --name redis -p 6379:6379 --network ctf_network redis

# 3. Start API server
docker run -d --name ctf_api -p 8000:8000 --network ctf_network ctf_api

# 4. Start Celery worker
docker run -d --name ctf_celery \
  -v //var/run/docker.sock:/var/run/docker.sock \
  --network ctf_network ctf_api \
  celery -A ctf_api worker --loglevel=info

# 5. Verify running containers
docker ps
```

---

## 📬 API Testing via Postman

### 📌 Assign a container
```json
POST /api/assign/
{
  "team_id": "team2",
  "challenge_id": "juice"
}
```

### 📌 Remove a container
```json
DELETE /api/remove/
{
  "team_id": "team2",
  "challenge_id": "juice"
}
```

### 📌 List all containers
```
GET /api/list/
```

---

## 📺 Video Demonstration

- [x] API interaction via Postman
- [x] Containers starting/stopping in `docker ps`
- [x] Celery logs showing task execution
- [x] Database records updating

👉 **video link**

---

## 📝 Notes

- Ensure the Docker socket `//var/run/docker.sock` is accessible.
- Use Django Admin or fixtures to preload team/challenge data.
- Adjust container ports or images as per your actual challenge setup.

---

**Built with** **Django**, 🐳 **Docker**, ⚙️ **Celery**, and 🧠 **Redis**
