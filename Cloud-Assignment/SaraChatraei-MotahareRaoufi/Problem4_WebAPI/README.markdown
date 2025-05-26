# Web API for Team Challenge Management

I developed a Web API to manage Capture The Flag (CTF) challenge containers for different teams, as part of my assignment. This document explains how I built the API, including the purpose of each endpoint, the database schema, how I configured Celery with Redis, and instructions to set it up and run it. I used Docker containers for both Redis and PostgreSQL to ensure a consistent environment.

---

## Overview of My API

I built this API using **FastAPI**, a Python web framework, to manage CTF challenge containers for teams. The API assigns and removes Docker containers based on team IDs and challenge IDs. Here's what my API does:

- Stores assignment data in a **PostgreSQL** database running in a Docker container.
- Uses **Celery** with **Redis** (also in a Docker container) to handle container management tasks asynchronously.
- Interacts with **Docker** to start and stop containers.
- Returns container addresses in responses so teams can access their challenges.

My API meets all the assignment requirements by:

- Assigning containers to teams based on team and challenge IDs.
- Removing containers when requested.
- Updating the database to track assignments.
- Processing container operations asynchronously using Celery and Redis.

---


## API Endpoints

I implemented two endpoints to manage CTF containers:

### 1. POST /assign

**What It Does**: This endpoint assigns a Docker container for a CTF challenge to a team.

- **Input**:
  - `team_id`: A string to identify the team.
  - `challenge_id`: A string to identify the challenge.
- **How It Works**:
  - Starts a Docker container using the `python:3.12` image through a Celery task.
  - Saves the team ID, challenge ID, container ID, and container IP address in the database.
  - Returns the container's IP address and a status message.
- **Response**:

  ```json
  {
    "status": "assigned",
    "container_address": "<container_ip>"
  }
  ```

### 2. POST /remove

**What It Does**: This endpoint removes a container assigned to a team for a specific challenge.

- **Input**:
  - `team_id`: A string to identify the team.
  - `challenge_id`: A string to identify the challenge.
- **How It Works**:
  - Checks the database for the container ID linked to the team and challenge.
  - Stops and removes the container using a Celery task.
  - Deletes the assignment from the database.
  - Returns a status message.
- **Response**:

  ```json
  {
    "status": "removed"
  }
  ```

  If no assignment exists:

  ```json
  {
    "status": "not found"
  }
  ```

---

## Database Schema

I used a **PostgreSQL** database (running in a Docker container) with one table called `assignments` to store container assignment details.

### Table: assignments

| Column | Data Type | Description |
| --- | --- | --- |
| `id` | SERIAL | Auto-incremented primary key. |
| `team_id` | VARCHAR(50) | The team's identifier. |
| `challenge_id` | VARCHAR(50) | The challenge's identifier. |
| `container_id` | VARCHAR(100) | The Docker container's unique ID. |
| `container_address` | VARCHAR(100) | The container's IP address. |

I designed the table to be created automatically when the `/assign` endpoint is called, using a `CREATE TABLE IF NOT EXISTS` statement to avoid errors if the table already exists.

---

## My Celery and Redis Configuration

I used **Celery** for asynchronous task processing and **Redis** (in a Docker container) as the message broker and result backend.

### How I Configured It

- **Broker**: Redis at `redis://localhost:6379/0` handles task queuing.
- **Backend**: Redis at `redis://localhost:6379/0` stores task results.
- **Tasks**:
  - `start_container`: Starts a Docker container and returns its ID and IP address.
  - `stop_container`: Stops and removes a Docker container by its ID.

### How It Works

- When I call the `/assign` endpoint, it queues a `start_container` task in Celery. The API waits up to 20 seconds for the task to finish and gets the container details.
- When I call the `/remove` endpoint, it queues a `stop_container` task to stop and remove the container. This runs asynchronously, so the API doesn't wait for it to complete.

---

## Explanation of My Code

### main.py

This file contains my FastAPI application and database logic.

#### Imports

```python
from fastapi import FastAPI, Depends
from tasks import start_container, stop_container
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
```

- `FastAPI` and `Depends`: For building the API and managing dependencies.
- `start_container`, `stop_container`: My Celery tasks from `tasks.py`.
- `create_engine`, `text`, `sessionmaker`: SQLAlchemy tools for database operations.

#### Database Setup

```python
DATABASE_URL = "postgresql://mot:mypassword@localhost:5432/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

- `DATABASE_URL`: Connects to my PostgreSQL container (`user:password@host:port/dbname`).
- `create_engine`: Sets up the database connection.
- `SessionLocal`: Creates a session factory for database interactions.

#### Dependency Injection

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- I created `get_db` to provide a database session for each request and close it afterward.

#### Endpoint: /assign

```python
@app.post("/assign")
async def assign_challenge(team_id, challenge_id, db=Depends(get_db)):
    image_name = "python:3.12"
    task = start_container.delay(image_name, team_id, challenge_id)
    result = task.get(timeout=20)
```

- **What It Does**: Assigns a container for a challenge to a team.
- **How It Works**:
  - Queues the `start_container` Celery task with the `python:3.12` image.
  - Waits up to 20 seconds for the task to return the container ID and IP address.

```python
    create_table_sql = text("""
    CREATE TABLE IF NOT EXISTS assignments (
        id SERIAL PRIMARY KEY,
        team_id VARCHAR(50),
        challenge_id VARCHAR(50),
        container_id VARCHAR(100),
        container_address VARCHAR(100)
    )
    """)
    db.execute(create_table_sql)
```

- Creates the `assignments` table if it doesn't exist, ensuring my database is ready.

```python
    insert_sql = text("""
    INSERT INTO assignments (team_id, challenge_id, container_id, container_address)
    VALUES (:team_id, :challenge_id, :container_id, :container_address)
    """)
    db.execute(insert_sql, {
        "team_id": team_id,
        "challenge_id": challenge_id,
        "container_id": result['container_id'],
        "container_address": result['container_address']
    })
    db.commit()
```

- Inserts the assignment details into the database and commits the changes.

```python
    return {"status": "assigned", "container_address": result['container_address']}
```

- Returns the assignment status and container IP address.

#### Endpoint: /remove

```python
@app.post("/remove")
async def remove_challenge(team_id, challenge_id, db=Depends(get_db)):
    query = text("SELECT container_id FROM assignments WHERE team_id=:team_id AND challenge_id=:challenge_id")
    container = db.execute(query, {"team_id": team_id, "challenge_id": challenge_id}).fetchone()
    if not container:
        return {"status": "not found"}
```

- **What It Does**: Removes a container for a team and challenge.
- **How It Works**:
  - Queries the database for the container ID.
  - Returns "not found" if no assignment exists.

```python
    stop_container.delay(container[0])
```

- Queues the `stop_container` task to stop and remove the container.

```python
    delete_query = text("DELETE FROM assignments WHERE team_id=:team_id AND challenge_id=:challenge_id")
    db.execute(delete_query, {"team_id": team_id, "challenge_id": challenge_id})
    db.commit()
```

- Deletes the assignment from the database and commits.

```python
    return {"status": "removed"}
```

- Returns a confirmation of removal.

### tasks.py

This file contains my Celery tasks for Docker container management.

#### Imports and Setup

```python
from celery import Celery
import docker

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0' 
)
client = docker.from_env()
```

- `Celery`: Sets up my Celery instance named `tasks`.
- `broker` and `backend`: Use my Redis container at `localhost:6379/0`.
- `docker.from_env()`: Connects to my Docker daemon.

#### Task: start_container

```python
@celery_app.task
def start_container(image_name, team_id, challenge_id):
    container = client.containers.run(image_name, detach=True, ports={'80/tcp': None})
    container.reload()
    container_ip = container.attrs['NetworkSettings']['IPAddress']
    return {'container_id': container.id, 'container_address': container_ip}
```

- **What It Does**: Starts a Docker container and returns its ID and IP address.
- **How It Works**:
  - Runs a container in detached mode with the given image.
  - Reloads the container to get updated attributes.
  - Extracts the container's IP address.
  - Returns the container ID and IP address.

#### Task: stop_container

```python
@celery_app.task
def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
    return {'status': 'removed'}
```

- **What It Does**: Stops and removes a Docker container.
- **How It Works**:
  - Gets the container by ID.
  - Stops and removes it.
  - Returns a confirmation status.

---

## How to Set Up and Run My API

I designed my API to run with Redis and PostgreSQL in Docker containers. Here's how to set it up:

### What You Need

- **Python 3.12**: Install Python 3.12 or later.
- **Docker**: Install Docker and ensure the daemon is running.
- **Python Packages**:

  ```bash
  pip install fastapi uvicorn sqlalchemy psycopg2-binary celery docker
  ```

### Step-by-Step Setup

1. **Run PostgreSQL in a Docker Container**:

   ```bash
   docker run -d --name postgres -p 5432:5432 -e POSTGRES_USER=mot -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb postgres:latest
   ```

   - This starts PostgreSQL with user `mot`, password `mypassword`, and database `mydb`.

2. **Run Redis in a Docker Container**:

   ```bash
   docker run -d --name redis -p 6379:6379 redis:latest
   ```

   - This starts Redis on `localhost:6379`.

3. **Save My Code**:

   - Create a project directory.
   - Save my `main.py` and `tasks.py` files in it.

4. **Pull the Python Image**:

   ```bash
   docker pull python:3.12
   ```

   - Ensures the `python:3.12` image is available for containers.

5. **Start the Celery Worker**:

   - In the project directory, run:

     ```bash
     celery -A tasks.celery_app worker --loglevel=info
     ```

6. **Start the FastAPI Server**:

   - In another terminal, in the project directory, run:

     ```bash
     uvicorn main:app --reload
     ```

   - My API will be available at `http://localhost:8000`.

---

## Testing API with Postman

I tested my API using Postman to ensure it works as expected.

### Test 1: Assign a Container

1. **Request**:
   - Method: POST
   - URL: `http://localhost:8000/assign`
   - Body (JSON):

     ```json
     {
       "team_id": "team1",
       "challenge_id": "challenge1"
     }
     ```
2. **Expected Response**:

   ```json
   {
     "status": "assigned",
     "container_address": "<container_ip>"
   }
   ```
3. **Verification**:
   - Check running containers:

     ```bash
     docker ps
     ```
   - Query the database:

     ```bash
     docker exec -it postgres psql -U mot -d mydb -c "SELECT * FROM assignments;"
     ```

### Test 2: Remove a Container

1. **Request**:
   - Method: POST
   - URL: `http://localhost:8000/remove`
   - Body (JSON):

     ```json
     {
       "team_id": "team1",
       "challenge_id": "challenge1"
     }
     ```
2. **Expected Response**:

   ```json
   {
     "status": "removed"
   }
   ```
3. **Verification**:
   - Check stopped containers:

     ```bash
     docker ps -a
     ```
   - Query the database to confirm deletion:

     ```bash
     docker exec -it postgres psql -U mot -d mydb -c "SELECT * FROM assignments;"
     ```

### Test 3: Remove Non-Existent Assignment

1. **Request**:
   - Method: POST
   - URL: `http://localhost:8000/remove`
   - Body (JSON):

     ```json
     {
       "team_id": "team2",
       "challenge_id": "challenge2"
     }
     ```
2. **Expected Response**:

   ```json
   {
     "status": "not found"
   }
   ```


## Explaination video

The video is avalable in https://iutbox.iut.ac.ir/index.php/s/iGPckqFZkxKJZcW