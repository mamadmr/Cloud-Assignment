# CTF Challenge Management Web API

This project provides a web API for managing CTF challenge containers for different teams, integrating a database, Celery with Redis for asynchronous tasks, and Docker for container management.

## Purpose of Each Endpoint

- **POST /api/assign/**: Assigns a specific CTF container to a team based on provided `team_id` and `challenge_id`. Returns a task ID and confirmation message.
- **DELETE /api/remove/**: Removes a CTF container from a team using the `team_id` and `challenge_id`. Returns a success message.
- **GET /api/list/**: Lists all active container assignments for teams, showing container details.

## Database Schema

- **Team**: Stores team information with fields including `id` (primary key) and other team details.
- **Challenge**: Stores challenge information with fields including `id` (primary key) and `image` (Docker image name).
- **Container**: Tracks active containers with fields including `id` (primary key), `team_id` (foreign key), `challenge_id` (foreign key), `container_id` (Docker container ID), and `address` (container access URL).

## Celery and Redis Configuration

- **Celery**: Configured to handle asynchronous tasks for starting and stopping Docker containers, using Redis as the message broker and result backend.
- **Redis**: Acts as the message broker for Celery, ensuring task queuing and result storage.

## Instructions to Set Up and Run the API

### Prerequisites
- Docker and Docker Desktop installed.
- Python 3.9 environment.
- Postman or similar API testing tool.

### Step-by-Step Setup

1. **Build the Docker Image**  
   - Command: `docker build -t ctf_api .`  
   - Purpose: Builds the API image with all dependencies, including Django, Celery, and required Python packages.

2. **Start the Redis Service**  
   - Command: `docker run -d --name redis -p 6379:6379 --network ctf_network redis`  
   - Purpose: Launches the Redis container as the message broker, accessible on port 6379 and within the `ctf_network`.

3. **Start the API Web Server**  
   - Command: `docker run -d --name ctf_api -p 8000:8000 --network ctf_network <your_api_image>`  
   - Purpose: Runs the Django API server, mapping port 8000 and connecting to the `ctf_network`. Replace `<your_api_image>` with the appropriate image name if different from `ctf_api`.

4. **Run the Celery Worker**  
   - Command: `docker run -d --name ctf_celery -v //var/run/docker.sock:/var/run/docker.sock --network ctf_network ctf_api celery -A ctf_api worker --loglevel=info`  
   - Purpose: Launches the Celery worker container, mounting the Docker socket for container management and connecting to the `ctf_network` for Redis communication.

5. **Verify Services**  
   - Command: `docker ps`  
   - Purpose: Checks that all containers (API, Celery worker, Redis) are running.

6. **Test the API with Postman**  
   - **Assign Container**: Send a POST request to `http://localhost:8000/api/assign/` with JSON `{"team_id": "team2", "challenge_id": "juice"}`.
   - **Remove Container**: Send a DELETE request to `http://localhost:8000/api/remove/` with JSON `{"team_id": "team2", "challenge_id": "juice"}`.
   - **List Containers**: Send a GET request to `http://localhost:8000/api/list/`.
   - Purpose: Confirms API functionality and container management.

7. **Check Logs**  
   - Command: `docker logs ctf_celery`  
   - Purpose: Reviews Celery worker logs to verify task execution.

8. **Stop Services**  
   - Command: `docker stop ctf_celery ctf_api redis`  
   - Purpose: Stops the running containers.
   - Command: `docker rm ctf_celery ctf_api redis`  
   - Purpose: Removes the stopped containers.

### Notes
- Ensure the Docker socket (`//var/run/docker.sock`) is accessible on your system (common in WSL2 with Docker Desktop).
- Populate the database with initial team and challenge data via Django admin or migrations.
- The API server command assumes a pre-built image; adjust the run command if your setup differs (e.g., includes a specific entrypoint).