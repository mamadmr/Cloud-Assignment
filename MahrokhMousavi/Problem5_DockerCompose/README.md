# CTF Challenge Management Web API - Docker Compose Integration

This document covers the Docker Compose integration for the CTF Challenge Management Web API, orchestrating PostgreSQL, Redis, Celery, the Django web API, and CTF challenge containers into a single cohesive system.

---

## 📘 Table of Contents
- [Docker Compose Setup](#docker-compose-setup)
- [System Initialization and Operation](#system-initialization-and-operation)
- [Video Demonstration](#video-demonstration)

---

## 🐳 Docker Compose Setup

### docker-compose.yml
The `docker-compose.yml` file defines all services required for the system:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:latest
    environment:
      - POSTGRES_USER=ctf_user
      - POSTGRES_PASSWORD=ctf_password
      - POSTGRES_DB=ctf_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - ctf_network

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    networks:
      - ctf_network

  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 ctf_api.wsgi:application
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=ctf_api.settings
    depends_on:
      - postgres
      - redis
    networks:
      - ctf_network

  celery:
    build: .
    command: celery -A ctf_api worker --loglevel=info
    volumes:
      - .:/app
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DJANGO_SETTINGS_MODULE=ctf_api.settings
    depends_on:
      - postgres
      - redis
    networks:
      - ctf_network

  challenge_todo:
    image: jetty:9.4-jre11-slim
    ports:
      - "14480:8080"
    networks:
      - ctf_network
    deploy:
      replicas: 0  # Start with no instances, managed by the API

  challenge_juice:
    image: bkimminich/juice-shop
    ports:
      - "14528:3000"
    networks:
      - ctf_network
    deploy:
      replicas: 0  # Start with no instances, managed by the API

networks:
  ctf_network:
    driver: bridge

volumes:
  pgdata:
```

#### Architecture Explanation
The system is composed of five main services, all connected via a bridge network (`ctf_network`) to ensure seamless communication. Below is a detailed breakdown of each service, its role, and how they interact:

- **postgres**:
  - **Role**: Acts as the persistent database for the system, storing information about teams, challenges, and containers.
  - **Credentials**: Uses `ctf_user` as the username and `ctf_password` as the password, with the database named `ctf_db`.
  - **Port**: Exposes port `5432` for database access.
  - **Persistence**: Uses a volume (`pgdata`) to ensure data persists across container restarts.
  - **Interaction**: The `web` service (Django API) connects to `postgres` to store and retrieve data about teams, challenges, and active containers.

- **redis**:
  - **Role**: Serves as the message broker for Celery, handling task queuing for asynchronous operations like starting and stopping containers.
  - **Port**: Exposes port `6379` for communication.
  - **Interaction**: The `celery` service connects to `redis` to queue and process tasks, such as container management tasks triggered by the `web` service.

- **web**:
  - **Role**: Runs the Django-based API server using Gunicorn, providing endpoints to assign, remove, and list challenges.
  - **Port**: Exposes port `8000` for API access (e.g., `http://localhost:8000/api/assign/`).
  - **Dependencies**: Depends on `postgres` for database operations and `redis` for task queuing via Celery.
  - **Interaction**: Receives HTTP requests from users (via Postman), interacts with `postgres` to manage data, and sends tasks to `celery` via `redis` for container management.

- **celery**:
  - **Role**: Executes asynchronous tasks, such as starting and stopping challenge containers, using the Celery worker.
  - **Docker Socket**: Mounts `/var/run/docker.sock` to interact with the Docker daemon and manage containers.
  - **Dependencies**: Depends on `postgres` and `redis` to process tasks and store results.
  - **Interaction**: Receives tasks from the `web` service via `redis`, manages challenge containers (`challenge_todo`, `challenge_juice`), and updates `postgres` with container details.

- **challenge_todo** and **challenge_juice**:
  - **Role**: Represent the CTF challenge containers (`jetty:9.4-jre11-slim` for Todo App, `bkimminich/juice-shop` for Juice Shop).
  - **Ports**: Map host ports `14480` to container port `8080` (Todo App) and `14528` to `3000` (Juice Shop) for consistent access.
  - **Replicas**: Start with `replicas: 0`, meaning they are not running initially; the `celery` service dynamically starts them when the API assigns a challenge.
  - **Interaction**: Managed by `celery`, which starts and stops these containers based on API requests. They join the `ctf_network` for accessibility.

#### Service Connections
- All services are connected via the `ctf_network` bridge network, allowing them to communicate using their service names (e.g., `postgres`, `redis`).
- The `web` service sends HTTP responses to users and delegates container management tasks to `celery` via `redis`.
- The `celery` service interacts with the Docker daemon to start/stop challenge containers and updates the `postgres` database with container details (e.g., `container_id`, `address`).

#### Architecture Diagram
The chart below visualizes the structure and connections between services using bars to represent services and implied connections:

```chartjs
{
  "type": "bar",
  "data": {
    "labels": ["postgres", "redis", "web", "celery", "challenge_todo", "challenge_juice"],
    "datasets": [
      {
        "label": "Services",
        "data": [1, 1, 1, 1, 1, 1],
        "backgroundColor": ["#4CAF50", "#FF5733", "#2196F3", "#FFC107", "#9C27B0", "#9C27B0"],
        "borderColor": ["#000", "#000", "#000", "#000", "#000", "#000"],
        "borderWidth": 1
      },
      {
        "label": "Connections (Implied)",
        "data": [0, 0, 0, 0, 0, 0],
        "backgroundColor": "rgba(0,0,0,0)",
        "borderColor": "#666",
        "borderWidth": 1,
        "type": "line",
        "fill": false,
        "pointRadius": 0,
        "segment": {
          "borderDash": [5, 5]
        },
        "data": [
          {"x": 0, "y": 0}, {"x": 2, "y": 0}, // postgres to web
          {"x": 1, "y": 0}, {"x": 2, "y": 0}, // redis to web
          {"x": 1, "y": 0}, {"x": 3, "y": 0}, // redis to celery
          {"x": 3, "y": 0}, {"x": 4, "y": 0}, // celery to challenge_todo
          {"x": 3, "y": 0}, {"x": 5, "y": 0}  // celery to challenge_juice
        ]
      }
    ]
  },
  "options": {
    "plugins": {
      "legend": {
        "display": false
      },
      "tooltip": {
        "enabled": false
      }
    },
    "scales": {
      "x": {
        "title": {
          "display": true,
          "text": "Services"
        }
      },
      "y": {
        "display": false,
        "min": 0,
        "max": 2
      }
    }
  }
}
```

This `bar` chart:
- **Bars**: Represent each service (`postgres`, `redis`, `web`, `celery`, `challenge_todo`, `challenge_juice`) with distinct colors.
- **Connections**: Uses a secondary line dataset with dashed lines to imply interactions (e.g., `postgres` to `web`, `celery` to `challenge_todo`), avoiding clutter while indicating relationships.
- **Labels**: The x-axis labels clearly identify each service, eliminating confusion.

---

## 🚀 System Initialization and Operation

### Prerequisites
- Docker installed
- Docker Compose installed
- Postman or curl

### Step-by-Step
1. Place the `docker-compose.yml` in your project directory.
2. Build and start all services:
   ```bash
   docker-compose up --build
   ```
3. Apply database migrations:
   ```bash
   docker exec ctf_web_1 python manage.py makemigrations
   docker exec ctf_web_1 python manage.py migrate
   ```
4. Fill the database with initial data:
   ```bash
   docker exec -it ctf_web_1 python manage.py shell
   ```
   In the shell:
   ```python
   from challenges.models import Team, Challenge
   Team.objects.create(team_id="team1", name="Team1")
   Team.objects.create(team_id="team2", name="Team2")
   Challenge.objects.create(challenge_id="todo", name="Todo App", image="jetty:9.4-jre11-slim", port=8080)
   Challenge.objects.create(challenge_id="juice", name="Juice Shop", image="bkimminich/juice-shop", port=3000)
   exit()
   ```
5. Verify running containers:
   ```bash
   docker ps
   ```
6. Use Postman to interact with the API (see below for test cases).

### API Testing via Postman
#### Assign a Container
- **Team2 - Juice Shop**:
  ```json
  POST /api/assign/
  {
    "team_id": "team2",
    "challenge_id": "juice"
  }
  ```
- **Team1 - Todo App**:
  ```json
  POST /api/assign/
  {
    "team_id": "team1",
    "challenge_id": "todo"
  }
  ```

#### Remove a Container
```json
DELETE /api/remove/
{
  "team_id": "team2",
  "challenge_id": "juice"
}
```

#### List All Containers
```
GET /api/list/
```

---

## 🎥 Video Demonstration

📎 [Click here to view the video](https://iutbox.iut.ac.ir/)

### Video Content (up to 5 minutes, Silent with Text Annotations)
This video is a silent demonstration with text annotations referring to this README for the architecture explanation. It shows the following steps:
- **System Startup**: Run `docker-compose up --build` and verify with `docker ps`.
- **Challenge Assignment**:
  - Assign challenges for Team1 (Todo App) and Team2 (Juice Shop) via Postman.
  - Show the resulting container creation in `docker ps`.
- **Challenge Removal**:
  - Remove the Juice Shop challenge for Team2 via Postman.
  - Confirm removal in `docker ps`.
- **Celery Logs**: Display `docker logs ctf_celery_1` to show container creation and removal logs.

---

## Notes
- Ensure the Docker socket `/var/run/docker.sock` is accessible.
- Configure `DJANGO_SETTINGS_MODULE=ctf_api.settings` in your environment or settings file to connect to PostgreSQL with the credentials `ctf_user` and `ctf_password`.
- Adjust container ports or images as per your actual challenge setup.

---
