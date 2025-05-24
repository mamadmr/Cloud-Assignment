# API Documentation: CTF Container Management System

---

## API Endpoints

### POST `/assign`
- **Purpose**: Assigns a CTF Docker container to a team and challenge using Celery
- **Request Body**:
  ```json
  {
    "team_id": "string",
    "challenge_id": "string"
  }
  ```

### DELETE `/remove`
- **Purpose**: Stops and removes a Docker container linked to a team and challenge
- **Request Body**:
  ```json
  {
    "team_id": "string",
    "challenge_id": "string"
  }
  ```

### POST `/background/assign`
- **Purpose**: Initiates container assignment as a background task without waiting for completion
- **Request Body**:
  ```json
  {
    "team_id": "string",
    "challenge_id": "string"
  }
  ```

---

## Database Schema

**Database File**: `containers.db` (SQLite)  
**ORM Definition**: `database.py`

### Table: `containers`
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `team_id` | String | ID of the team assigned the container |
| `challenge_id` | String | ID of the challenge |
| `container_id` | String | Docker container ID |
| `host_port` | String | Host port mapped to container port 80 |
| `status` | String | Either `"active"` or `"removed"` |

**Inspection Command**:
```bash
sqlite3 containers.db "SELECT * FROM containers;"
```

---

## Celery & Redis Configuration

### Celery Configuration File (`celery_worker.py`)
```python
from celery import Celery

celery_app = Celery(
    "ctf_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
```

### Key Components
- **Redis**: Serves as both message broker and result backend (default port: 6379)
- **Tasks**:
  - `start_ctf_container`: Creates Docker container and updates database
  - `stop_ctf_container`: Removes container and updates status

### Start Celery Worker
```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

---


### Initialization Steps
1. Start Redis:
   ```bash
   redis-server
   ```
2. Initialize Database:
   ```bash
   python database.py
   ```
3. Start API Server:
   ```bash
   uvicorn main:app --reload
   ```
4. Start Celery Worker:
   ```bash
   celery -A celery_worker.celery_app worker --loglevel=info
   ```

---

## Usage Examples

### Assign Container
```bash
curl -X POST http://localhost:8000/assign \
    -H "Content-Type: application/json" \
    -d '{"team_id": "team1", "challenge_id": "chal1"}'
```

### Remove Container
```bash
curl -X DELETE http://localhost:8000/remove \
    -H "Content-Type: application/json" \
    -d '{"team_id": "team1", "challenge_id": "chal1"}'
```

---

