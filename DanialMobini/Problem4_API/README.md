# CTF Challenge Management API

## (i)

### (a)

**Endpoints to implement:**

```http
POST   /assign-container        # Assign a CTF container to a team
DELETE /remove-container        # Remove the CTF container from a team
```

**Request Format Example:**

```json
POST /assign-container
{
  "team_id": 1,
  "challenge_id": "juice-shop"
}
```

**Response Format:**

```json
{
  "message": "Container started successfully",
  "address": "http://localhost:PORT"
}
```

### (b)

#### Database Schema (PostgreSQL)

```sql
-- teams table
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- challenges table
CREATE TABLE challenges (
    id TEXT PRIMARY KEY,
    image_name TEXT
);

-- team_challenges table (many-to-many relationship)
CREATE TABLE team_challenges (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id),
    challenge_id TEXT REFERENCES challenges(id),
    container_id TEXT,
    address TEXT,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, challenge_id)
);

-- Inserting sample teams
INSERT INTO teams (name) VALUES 
('Red Team'),
('Blue Team'),
('Green Team'),
('White Team'),
('Black Team');

-- Inserting sample challenges
INSERT INTO challenges (id, image_name) VALUES 
('nginx','nginx:latest')
('juice-shop', 'bkimminich/juice-shop'),
('dvwa', 'vulnerables/web-dvwa'),
('metasploitable', 'tleemcjr/metasploitable2'),
('webgoat', 'webgoat/webgoat-8.0'),
('hackazon', 'ianwijaya/hackazon');

```

### (c)

#### Celery Tasks

Create a `tasks.py`:

```python
from celery import Celery
import docker

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)
client = docker.from_env()

@app.task
def start_container(team_id, challenge_id, image_name):
    container = client.containers.run(image_name, detach=True, ports={"3000/tcp": None})
    return {
        "container_id": container.id,
        "address": f"http://localhost:{container.attrs['NetworkSettings']['Ports']['3000/tcp'][0]['HostPort']}",
    }

@app.task
def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
    return True

```

### (d)

#### Instructions

-1 **Start Redis**

```bash
docker run --rm -d -p 6379:6379/tcp my_redis_server:latest`
```

-2 **Start PostgreSQL**

```bash
docker run --rm -d -p 5432:5432/tcp postgres_ctf:latest
```

-3 **Start the Celery Worker**

```bash
celery -A tasks worker --loglevel=info
```

-4 **Run the Flask App**

```bash
export FLASK_APP=app.py
flask run
```

```bash
psql -h localhost -U admin -d ctf_db
```

#### API

**Assign a container:**

```bash
curl -X POST http://localhost:5000/assign-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "juice-shop"}'

curl -X POST http://localhost:5000/assign-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "nginx"}'
```

**Remove a container:**

```bash
curl -X DELETE http://localhost:5000/remove-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "juice-shop"}'

curl -X DELETE http://localhost:5000/remove-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "nginx"}'
```

## (ii) 🎥 Video Demonstration

[Video](https://iutbox.iut.ac.ir/index.php/s/k5fGsR3bRnf2n68)
