
---

# 🚀 SOLI_CTF API

A containerized microservice project using **FastAPI**, **Celery**, **PostgreSQL**, **Redis**, and **Docker** to manage task assignments between teams and challenges. Tasks are executed by dynamically launching and managing Docker containers per team-challenge assignment.

---

## 📁 Project Structure

```
.
├── src/
│   ├── api/                # FastAPI routes
│   │   └── routes.py
│   ├── config/             # Configuration and DB setup
│   │   ├── db.py
│   │   └── settings.py
│   ├── entities/           # SQLAlchemy models
│   │   ├── assignment.py
│   │   ├── task.py
│   │   └── team.py
│   ├── schemas/            # Pydantic models
│   │   ├── assignment_schema.py
│   │   ├── task_schema.py
│   │   └── team_schema.py
│   ├── workers/            # Celery and Docker task logic
│   │   ├── celery_instance.py
│   │   └── docker_tasks.py
│   └── app.py              # FastAPI app entry point
├── Dockerfile.web          # Dockerfile for FastAPI app
├── Dockerfile.celery       # Dockerfile for Celery worker
├── docker-compose.yml      # Multi-container orchestration
├── requirements.txt        # Python dependencies
```

---

## ⚙️ Technologies Used

* **FastAPI** – RESTful API framework
* **Celery** – Asynchronous task queue
* **Redis** – Broker and result backend for Celery
* **Docker** – For container orchestration and runtime
* **PostgreSQL** – Relational database
* **SQLAlchemy** – ORM for database interaction
* **Pydantic** – Data validation and schema definition

---

## 🧠 Key Features

* Create teams and tasks
* Assign a task (challenge) to a team
* Launch a Docker container for the assignment asynchronously using Celery
* Terminate the container on request
* Retrieve current assignments
* Filter assignments by team
* Fully dockerized and production-ready

---

## 🧰 Setup & Usage

### 🚨 Prerequisites

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

### 🔧 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/rasoul6094/Cloud-Assignment.git
   cd  Cloud-Assignment
   cd  soli-ctf/Cloud-Assignment/soli-ctf/q4
   ```

2. **Run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

3. **Access the API**

   * Base URL: `http://localhost:8000`
   * Interactive Docs: `http://localhost:8000/docs`

---

## 🔄 API Endpoints

### 🔗 Assignments

* `POST /api/v1/assign` – Assign a task to a team (launches Docker container)
* `POST /api/v1/remove` – Remove an assignment (stops/removes Docker container)
* `GET /api/v1/assignments` – List all assignments (or filter by `team_id`)
* `GET /api/v1/assignment` – Get specific assignment by `team_id` and `challenge_id`

### 🔗 Tasks

* `POST /api/v1/tasks` – Create a new task
* `GET /api/v1/tasks` – List all tasks

### 🔗 Teams

* `POST /api/v1/teams` – Create a new team
* `GET /api/v1/teams` – List all teams

---

## 🧪 Example Request

```json
POST /api/v1/assign
{
  "team_id": 1,
  "task_id": 2
}
```

Response:

```json
{
  "team_id": 1,
  "challenge_id": 2,
  "container_name": "team1_task2",
  "container_url": "http://localhost:3020",
  "status": "starting"
}
```

---

## 📦 Dockerized Services

* `postgres_db` – PostgreSQL DB container
* `redis_broker` – Redis as Celery broker/backend
* `web_app` – FastAPI backend
* `celery_worker` – Worker for Docker container tasks

---

## 🧠 How Redis is Used

Redis is used as both the **broker** and the **result backend** for Celery. It enables task queuing and result storage for asynchronous operations such as:

* Launching Docker containers (`launch_container`)
* Terminating Docker containers (`terminate_container`)

Configuration (see `src/workers/celery_instance.py`):

```python
celery_app = Celery(
    "docker_tasks",
    broker="redis://redis_broker:6379/0",
    backend="redis://redis_broker:6379/0"
)
```

---

## 🧹 Clean Shutdown

To bring down all containers:

```bash
docker-compose down
```

To remove volumes as well:

```bash
docker-compose down -v
```


---

## 👨‍💻 Author

 – [Rasoul_Salehi(soli)](https://github.com/rasoul6094)

---

