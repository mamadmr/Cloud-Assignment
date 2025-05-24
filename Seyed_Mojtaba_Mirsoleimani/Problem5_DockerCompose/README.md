
# 🧠 CTF Challenge Management System – Docker Compose Integration

This project is part of a larger assignment to build and deploy a full-stack **Web API system for CTF (Capture The Flag) challenge management** using:

- Flask for the web API
- PostgreSQL for persistent data storage
- Redis & Celery for asynchronous container management
- Docker & Docker Compose for orchestration
- Dockerized challenge containers assigned to CTF teams

---

## 📌 Problem Overview

This system allows assigning/removing CTF challenge containers to teams via an API. It supports background container operations using Celery and Redis. Data about active containers is stored in a PostgreSQL database.

### Features

- ✅ REST API to assign/remove containers for teams
- ✅ PostgreSQL integration to persist container assignments
- ✅ Redis as the Celery message broker
- ✅ Celery to manage Docker containers in the background
- ✅ Docker Compose for running the entire system with a single command

---

## 🐳 Docker Compose Setup

All services are defined in the `docker-compose.yml`:

### 🔧 Services

| Service      | Role                                              |
|--------------|---------------------------------------------------|
| `web`        | Flask API server                                  |
| `db`         | PostgreSQL database for storing container records |
| `redis`      | Message broker for Celery                         |
| `celery`     | Worker that manages Docker containers             |
| `challenge`  | Sample CTF container image                        |

### 🕸️ Networking

All containers are on the same `backend` network, allowing services to communicate via container names:

- Flask connects to `db` and `redis`
- Celery shares the same codebase and connects to Docker engine and Redis
- PostgreSQL uses a volume to persist data across restarts

---

## 🚀 How to Run the Project

> 📝 Prerequisites:  
> Docker, Docker Compose, Python (for local testing), and virtualenv

1. **Clone the repository**

```bash
git clone https://github.com/SeyedMojtaba1/Cloud-Assignment.git
cd Seyed_Mojtaba_Mirsoleimani/Problem5_DockerCompose
````

2. **Build and run with Docker Compose**

```bash
docker-compose up --build
```

3. **The following services will be available:**

* Web API: [http://localhost:5000](http://localhost:5000)
* PostgreSQL: exposed internally to `web` and `celery`
* Redis: used internally by Celery

4. **Using Postman**
   Use the following endpoints:

### ➕ POST `/assign`

```json
{
  "team_id": "team1",
  "challenge_id": "web100"
}
```

**Response:**

```json
{
  "message": "Container assigned successfully.",
  "container_address": "http://localhost:<port>"
}
```

### ➖ POST `/remove`

```json
{
  "team_id": "team1",
  "challenge_id": "web100"
}
```

**Response:**

```json
{
  "message": "Container removed successfully."
}
```

---

## 🧪 Testing & Validation

* ✅ Assign/remove containers using Postman
* ✅ Confirm container appears/disappears via `docker ps`
* ✅ Validate DB rows for active containers
* ✅ Logs show coordination between Flask API, Celery worker, Redis, and PostgreSQL

