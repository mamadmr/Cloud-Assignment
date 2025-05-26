The web service runs a FastAPI application (main.py) exposing HTTP endpoints (/health, /assign, /containers, /remove) to manage nginx containers. It connects to the host's Docker daemon via /var/run/docker.sock to perform container operations, interacts with the PostgreSQL database (db service) using SQLAlchemy (postgresql://ctfuser:ctfpassword@db:5432/ctfdb) to store container metadata, and indirectly uses Redis through the worker service for task queuing. The service is accessible on http://localhost:8001.
The worker service runs a Celery worker (tasks.py) to process asynchronous tasks (start_container, stop_container), accessing the Docker daemon and database similarly to the web service. The redis service acts as a message broker and result backend for Celery, facilitating task distribution, while the db service (PostgreSQL) persists container metadata in a containers table. All services communicate over a Docker network (problem5-3_default), with redis and db using persistent volumes (redis_data, postgres_data) and health checks to ensure readiness.
Starting the System


Set Docker Socket Permissions (temporary for testing):
sudo chmod 666 /var/run/docker.sock

Start Services:
docker-compose down -v  # Clear previous state
docker-compose up -d --build

Verify Services:
docker-compose ps


Check Logs (optional):
docker-compose logs web worker


Using the System
Interact with the system via HTTP requests to http://localhost:8001 using curl, Postman, or any HTTP client. Below are example curl commands:

Check Health:
curl -X GET http://localhost:8001/health

Expected: {"status":"OK","docker_ready":true}

Assign a Container:
curl -X POST http://localhost:8001/assign \
  -H "Content-Type: application/json" \
  -d '{"team_id": "team1", "challenge_id": "challenge1"}'

Expected: {"message":"Container started","container_id":"..."}

List Containers:
curl -X GET http://localhost:8001/containers

Expected: [{"id":1,"team_id":"team1","challenge_id":"challenge1","container_id":"...","status":"active"}]

Remove a Container:
curl -X DELETE http://localhost:8001/remove \
  -H "Content-Type: application/json" \
  -d '{"team_id": "team1", "challenge_id": "challenge1"}'

Expected: {"message":"Container removed"}

Monitor Logs:
docker-compose logs -f web worker


Stop the System:
docker-compose down -v

