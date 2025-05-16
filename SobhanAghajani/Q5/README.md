# 📦 System Overview
This system is a CTF (Capture The Flag) challenge container manager built using FastAPI, Docker, PostgreSQL, Celery, and Redis. It allows teams to launch and stop challenge containers on demand, track their status, and manage challenge resources through an API.

# 🔗 Service Connections
FastAPI (ctf_api service): The main web API that teams interact with. It handles HTTP requests for starting/stopping containers and querying status.

PostgreSQL: Stores team and container state information persistently.

Celery: Handles background tasks such as starting and stopping Docker containers asynchronously.

Redis: Acts as a message broker for Celery.

Docker Engine: Used by the API to launch challenge containers (e.g., Juice Shop or ToDo Java app) per team.

These services communicate over a shared Docker network defined in the docker-compose.yml.

# Video link
https://iutbox.iut.ac.ir/index.php/s/n2nsSkjxD78bPAM