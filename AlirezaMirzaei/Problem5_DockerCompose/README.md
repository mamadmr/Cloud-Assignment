# Problem 5: Docker Compose Integration – Full System README

## Overview

This project combines all components of a CTF (Capture The Flag) management system using Docker Compose. It consists of microservices for database management, Redis queueing, Celery-based task execution, a web API, and dynamic challenge containers.

## How Services Are Connected

The system is composed of four main services:

- **PostgreSQL** stores all persistent information, including which team is assigned to which challenge.
- **Redis** acts as the broker and result backend for Celery.
- **Celery** executes background tasks such as starting or stopping challenge containers.
- **FastAPI Web API** allows clients to assign and remove challenges via HTTP endpoints.

These services communicate internally through a shared Docker network, ensuring isolated and reliable inter-service communication. The Celery worker uses Docker SDK to manage containers based on requests received from the FastAPI service.

## How to Start and Use the System

1. Navigate to the `AlirezaMirzaei` root directory in your terminal.
2. Move into the `Problem5_DockerCompose` folder.
3. Ensure that the `.env` file exists inside `Problem4_WebAPI` and contains the required configuration.
4. Start the system with `docker-compose up --build`.
5. Use the Python script provided in `Problem4_WebAPI/test_api.py` or any HTTP client (like curl or Postman) to assign and remove challenges for different teams.

The API provides two main endpoints:

- `/assign` — Starts a challenge container and registers it.
- `/remove` — Stops the container and updates the database.

