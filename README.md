# CTF Challenge Manager

This project is a Capture The Flag (CTF) challenge manager that dynamically assigns and removes containerized challenges per team using FastAPI and Celery. It leverages Docker to isolate challenge environments and Redis + PostgreSQL for state and queue management.

## 🚀 About

This system allows teams to request specific CTF challenges. Upon request:
- A Docker container is launched with the challenge
- Metadata is stored in a PostgreSQL database
- Celery manages background tasks (container operations)
- Redis serves as both the Celery broker and result backend

## 🔧 Stack

- **FastAPI** – for building the REST API
- **Celery** – for background task processing
- **Docker SDK** – to start/stop containers
- **Redis** – Celery broker and result store
- **PostgreSQL** – data persistence for assigned challenges
- **Adminer** – GUI for PostgreSQL
- **RedisInsight** – GUI for Redis

## 📦 Features

- Assign a challenge (via Docker container) to a team
- Track the status of challenges (starting, stopping, etc.)
- Remove challenge containers safely
- View Redis and PostgreSQL data via browser UIs

## ▶️ Getting Started (Docker)

1. **Build and start services**:

```bash
docker compose up --build
```

2. **Access services**:
- API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Adminer: [http://localhost:8080](http://localhost:8080)
- RedisInsight: [http://localhost:5540](http://localhost:5540)

3. **Use Adminer**:
- System: PostgreSQL
- Server: `db`
- User: `FaezehGhiasi`
- Password: `1234`
- Database: `ctfdb`

## 🧪 API Endpoints

### `POST /api/v1/assign_challenge`

Assigns a Docker-based challenge to a team.

**Request body**:
```json
{
  "team_id": 1,
  "challenge_id": 2
}
```

### `POST /api/v1/remove_challenge`

Stops and removes a previously assigned challenge container.

**Request body**:
```json
{
  "team_id": 1,
  "challenge_id": 2
}
```

## ⚙️ Celery Tasks

- `start_container(image_name, container_name)`
- `stop_container(container_name)`

These tasks use the Docker SDK in async/background mode to manage containers.

## 📁 Volumes & Ports

- PostgreSQL data stored in `postgres_data` volume
- Ports:
  - 8000: FastAPI
  - 8080: Adminer
  - 5540: RedisInsight
  - 6379: Redis
  - 5432: PostgreSQL

## 📚 Notes

You must ensure Docker is accessible inside the `api` and `worker` containers via mounted Docker socket:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

## 👤 Author

Faezeh Ghiasi