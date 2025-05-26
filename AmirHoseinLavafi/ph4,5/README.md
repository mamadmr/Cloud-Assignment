🔗 API Endpoints
1. POST /assign
Purpose: Assigns a specific CTF container to a team based on the team_id and challenge_id.

Request Body:

{
  "team_id": 1,
  "challenge_id": 1
}

Response:

{
  "container_id": "abc123...",
  "address": "localhost:49154"
}

Behavior:
    Triggers a Celery task to start a Docker container.
    Stores the container ID and its exposed address in PostgreSQL.

2. POST /remove
Purpose: Removes a container assigned to a team for a given challenge.

Request Body:

{
  "team_id": 1,
  "challenge_id": 1
}

Response:

{
  "status": "removed"
}

Behavior:
    Triggers a Celery task to stop and remove the container.
    Deletes the corresponding record from the database.

🗄️ Database Schema

CREATE TABLE team_challenges (
    id SERIAL PRIMARY KEY,
    team_id INT,
    challenge_id INT,
    container_id TEXT,
    container_address TEXT,
    status TEXT DEFAULT 'running',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

⚙️ Celery & Redis Configuration

🚀 How to Run

    Start services:

    docker-compose up --build


    This initializes:
        Flask API on http://localhost:5000
        Redis on port 6379
        PostgreSQL on port 5432
        Celery worker to process task queue
        Docker socket access for container control


    Test API with Postman:

        Assign:
            POST to http://localhost:5000/assign
            JSON: { "team_id": 1, "challenge_id": 1 }
        
        Expected response:
            {
            "container_id": "xxx",
            "address": "localhost:49156"
            }

        Remove:
            POST to http://localhost:5000/remove
            JSON: { "team_id": 1, "challenge_id": 1 }

        Expected response:
            {
            "status": "removed"
            }

Networking and Service Access

All services run on a default Docker network created by Compose, which allows:
    Flask API to connect to db and redis using hostnames.
    Celery worker to access Redis and Docker daemon.
    Docker containers to be started dynamically and exposed via random ports on localhost.


