# Problem 5: Docker Compose Integration

This document describes how to integrate your API, Celery worker, PostgreSQL, Redis, and CTF challenge containers into a single `docker-compose` setup.

## Project Structure

```
project-root/
├── Problem4_API/
│   ├── api/         # FastAPI code + Dockerfile
│   └── worker/      # Celery tasks + Dockerfile
└── Problem5_docker-compose/
    └── docker-compose.yml
```

## `docker-compose.yml`

Place the following `docker-compose.yml` in `Q5/`:

```yaml
services:
  postgres:
    image: postgres:15
    container_name: ctf_db
    environment:
      POSTGRES_USER: ctftest
      POSTGRES_PASSWORD: ctftest
      POSTGRES_DB: ctfdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - ctf-net

  redis:
    image: redis:7-alpine
    container_name: ctf_redis
    networks:
      - ctf-net

  worker:
    build:
      context: ../Q4/worker
      dockerfile: Dockerfile
    container_name: ctf_worker
    depends_on:
      - redis
    environment:
      BROKER_URL: redis://ctf_redis:6379/0
      BACKEND_URL: redis://ctf_redis:6379/1
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - ctf-net

  api:
    build:
      context: ../Q4/api
      dockerfile: Dockerfile
    container_name: ctf_api
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://ctftest:ctftest@ctf_db:5432/ctfdb
      REDIS_URL: redis://ctf_redis:6379/0
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - ctf-net

volumes:
  pgdata:

networks:
  ctf-net:
    driver: bridge
```

### `services`

- **postgres**  
  - **image**: `postgres:15` pulls the official PostgreSQL v15 image.  
  - **environment**: Sets `POSTGRES_USER` / `PASSWORD` / `DB` for initial database creation.  
  - **volumes**: `pgdata` persists database files across restarts.  
  - **networks**: Attaches to the `ctf-net` network so other services can reach it by name.

- **redis**  
  - **image**: `redis:7-alpine` is a lightweight Redis v7 variant.  
  - **networks**: Joins `ctf-net` for broker connectivity.

- **worker**  
  - **build**:  
    - **context**: `../Q4/worker` – Dockerfile’s folder.  
    - **dockerfile**: Name of the Dockerfile to use.  
  - **depends_on**: Ensures Redis starts before the worker.  
  - **environment**:  
    - `BROKER_URL` and `BACKEND_URL` point Celery to Redis.  
  - **volumes**: Mounts the host’s Docker socket so the worker can launch challenge containers.  
  - **networks**: Uses `ctf-net`.

- **api**  
  - **build**:  
    - **context**: `../Q4/api` – your FastAPI code folder.  
    - **dockerfile**: Name of the Dockerfile.  
  - **depends_on**: Waits for Postgres and Redis.  
  - **ports**: Exposes port `8000` on the host.  
  - **environment**:  
    - `DATABASE_URL` tells your app how to connect to PostgreSQL.  
    - `REDIS_URL` for Celery broker connectivity.  
  - **volumes**: Also mounts the Docker socket so the API can inspect containers if needed.  
  - **networks**: Uses `ctf-net`.

### `volumes`
- **pgdata**  
  A named volume that holds PostgreSQL data so it isn’t lost when the container is recreated.

### `networks`
- **ctf-net**  
  A user-defined bridge network that all services share. This ensures they can reference each other by container name (e.g., `ctf_db`, `ctf_redis`) without publishing every port publicly.

## Steps to Build and Run

1. Change directory to `Problem5_docker-compose/`:
   ```bash
   cd ./Problem5_docker-compose
   ```
2. Build all services:
   ```bash
   docker-compose build
   ```
3. Start everything in detached mode:
   ```bash
   docker-compose up -d
   ```

## Verification

1. Check service status:
   ```bash
   docker-compose ps
   ```
2. View API logs:
   ```bash
   docker-compose logs -f api
   ```
3. Assign a challenge:
   ```bash
   curl -X POST http://localhost:8000/assign      -H "Content-Type: application/json"      -d '{"team_id":"teamA","challenge":"todo","image":"nginx"}'
   ```
4. Confirm container is running:
   ```bash
   docker ps --filter name=teamA-todo
   ```
5. Inspect database:
   ```bash
   docker exec -it ctf_db psql -U ctftest -d ctfdb      -c "SELECT * FROM team_challenges;"
   ```
6. Remove the challenge:
   ```bash
   curl -X POST http://localhost:8000/remove      -H "Content-Type: application/json"      -d '{"team_id":"teamA","challenge":"todo"}'
   ```

## Shutdown

To stop and remove all containers:
```bash
docker-compose down
```

> **Note:** The PostgreSQL volume remains by default. To remove it too, run:
> ```bash
> docker-compose down -v
> ```

