# CTF Challenge Management Service

This project implements a web API and background worker to manage CTF challenge containers for teams. It uses FastAPI, Celery with Redis, PostgreSQL, and Docker.

## Project Structure

```
Problem4_API/
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── models.py
├── worker/
│   ├── Dockerfile
│   └── tasks.py
└── README.md
```

## Docker Setup

### 1. Create Docker Network

```bash
docker network create ctf-net
```

### 2. Launch PostgreSQL

```bash
docker run -d   --name ctf_db   --network ctf-net   -e POSTGRES_USER=ctftest   -e POSTGRES_PASSWORD=ctftest   -e POSTGRES_DB=ctfdb   -v pgdata:/var/lib/postgresql/data   postgres:15
```

### 3. Launch Redis

```bash
docker run -d   --name ctf_redis   --network ctf-net   -p 6379:6379   redis:7
```

### 4. Build & Run Worker

```bash
cd worker
docker build -t ctf_worker .
docker run -d   --name ctf_worker   --network ctf-net   -v /var/run/docker.sock:/var/run/docker.sock   -e BROKER_URL=redis://ctf_redis:6379/0   -e BACKEND_URL=redis://ctf_redis:6379/1   ctf_worker
```

### 5. Build & Run API

```bash
cd api
docker build -t ctf_api .
docker run -d   --name ctf_api   --network ctf-net   -p 8000:8000   -v /var/run/docker.sock:/var/run/docker.sock   -e DATABASE_URL=postgresql+asyncpg://ctftest:ctftest@ctf_db:5432/ctfdb   -e REDIS_URL=redis://ctf_redis:6379/0   ctf_api
```

## Code Explanation

### `api/main.py`

- **FastAPI App**: Defines endpoints `/assign` and `/remove`.
- **Models**: Uses Pydantic schemas `AssignRequest` and `RemoveRequest`.
- **Database**: Async SQLAlchemy engine built with:
  ```python
  engine = create_async_engine(DATABASE_URL)
  ```
- **Celery Client**:
  ```python
  celery_app = Celery(
      "api",
      broker=os.getenv("REDIS_URL"),
      backend=os.getenv("REDIS_URL").replace("/0", "/1"),
  )
  ```
- **Assign Endpoint**:
  ```python
  @app.post("/assign")
  async def assign(req: AssignRequest):
      task = celery_app.send_task(
          "tasks.start_ctf",
          args=[req.image, req.team_id, req.challenge],
      )
      res = task.get(timeout=30)
      # Save to DB and return container_id, address
      ...
  ```
- **Remove Endpoint**:
  ```python
  @app.post("/remove")
  async def remove(req: RemoveRequest):
      celery_app.send_task("tasks.stop_ctf", args=[req.container_id])
      # Update DB status
      ...
  ```

### `worker/tasks.py`

- **Celery Worker App**:
  ```python
  app = Celery(
      "tasks",
      broker=os.getenv("BROKER_URL"),
      backend=os.getenv("BACKEND_URL"),
  )
  ```
- **start_ctf Task**:
  ```python
  @app.task
  def start_ctf(image: str, team_id: str, challenge: str) -> str:
      name = f"{team_id}-{challenge}"
      container = docker.from_env().containers.run(image, name=name, detach=True)
      return container.id
  ```
- **stop_ctf Task**:
  ```python
  @app.task
  def stop_ctf(container_id: str) -> bool:
      cont = docker.from_env().containers.get(container_id)
      cont.stop()
      cont.remove()
      return True
  ```

## Testing & Verification

1. **Assign Container**
   ```bash
   curl -X POST http://localhost:8000/assign      -H "Content-Type: application/json"      -d '{"team_id":"teamA","challenge":"todo","image":"nginx"}'
   ```
2. **Check Running Container**
   ```bash
   docker ps
   ```
3. **Inspect DB**
   ```bash
   docker exec ctf_db psql -U ctftest -d ctfdb      -c "SELECT * FROM team_challenges;"
   ```
4. **Remove Container**
   ```bash
   curl -X POST http://localhost:8000/remove      -H "Content-Type: application/json"      -d '{"container_id":"<id>"}'
   ```

