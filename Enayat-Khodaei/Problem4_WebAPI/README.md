# Web API for Team Challenge Management
This API allows teams to start and stop challenge containers dynamically using Docker, with task queuing handled by Celery and Redis, and state stored in PostgreSQL.

## Endpoints

### 1. `POST /assign`
- **Purpose**: Assign a Docker container to a team for a specific challenge.
- **Request Body (JSON)**:
  ```json
  {
    "team_id": "string",
    "challenge_id": "string",
    "image": "string"
  } 

- **Response**:
    On success: { "status": "success", "address": "http://localhost:<port>" }
    On error: { "status": "error", "message": "..." }

- An example of 'on success' message is attached to this file named 1.png.


### 2. `POST /remove`
- **Purpose**: Remove the container assigned to a team for a specific challenge.
- **Request Body (JSON)**:
  ```json
  {
    "team_id": "string",
    "challenge_id": "string"
  } 

- **Response**:
    On success: { { "status": "success", "message": "Container ... stopped and removed." } }
    On error: { "status": "error", "message": "..." }

- An example of 'on success' message is attached to this file named 2.png.

## Database Schema
    ```sql
    CREATE TABLE containers (
        id UUID PRIMARY KEY,
        team_id VARCHAR(50),
        challenge_id VARCHAR(50),
        container_id VARCHAR(100),
        address TEXT
    );

- "The picture of the Db is shown in 3.png file".


The application uses Redis as both the message broker and the result backend for Celery. The Redis server is running and accessible from the url: redis://localhost:6379/0
Before Starting the celery workers we need to start our redis server. We used the redis image to have a redis server from a container. Because we had this container before, We just needed to start this container. So we used the command below:
- docker start my-redis

After starting redis we need to start the celery. We used the command below:
- celery -A celery_worker.celery worker --loglevel=info --pool=solo
-A celery_worker.celery: Specifies the Celery instance to run, imported from the celery_worker.py file.
--loglevel=info: Sets the logging level for better visibility of task processing.
--pool=solo: Ensures compatibility in windows.

Next step is to launch the main API server (Flask), using the following command:
- python app.py


The following lines in app.py configure the Flask app to use Celery with Redis as both the message broker and the result backend:
- app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
- app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

CELERY_BROKER_URL: This tells Celery where to send tasks. Here, Redis is being used as the message broker. When you call a Celery task (e.g., start_container_task.delay(...)), that task is sent to Redis as a message.
CELERY_RESULT_BACKEND: This defines where to store the result of the task. Celery will write the result (success, failure, return value) back into Redis so that it can be retrieved later using task.get(). 


Initializing Celery
- celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
- celery.conf.update(app.config)

This creates a Celery application instance and connects it to the broker (Redis). By calling celery.conf.update(app.config), all relevant Flask configurations (such as the result backend) are passed to Celery as well.

In other words:
Flask sends background tasks to Redis → Celery worker listens to Redis → Executes the task (e.g., run a Docker container) → Stores result back in Redis.

