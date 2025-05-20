# Docker Compose Integration

## (2) System Explanation and Usage Guide

### Service Architecture

1. **PostgreSQL**: The primary database storing:
   - Challenge information (in `challenges` table)
   - Team-container assignments (in `team_challenges` table)

2. **Redis**: Message broker for Celery tasks:
   - Handles asynchronous container operations
   - Stores task results temporarily

3. **Web Service (Flask)**: The main API that:
   - Exposes REST endpoints for container management
   - Communicates with PostgreSQL for data
   - Queues tasks to Celery via Redis

4. **Celery Worker**: Handles background tasks:
   - Starts challenge containers using Docker API
   - Stops and removes containers when requested

### Service Connections

```
[Curl/Client] → [Web Service (Flask)]
                    │
                    ├──→ [PostgreSQL] (for data storage)
                    │
                    └──→ [Redis] → [Celery] → [Docker Engine]
```

#### API Endpoints

1. **Assign a Container**:

```bash
curl -X POST http://localhost:5000/assign-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "juice-shop"}'

curl -X POST http://localhost:5000/assign-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 2, "challenge_id": "nginx"}'
```

2. **Remove a Container**:

```bash
curl -X DELETE http://localhost:5000/remove-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 1, "challenge_id": "juice-shop"}'

curl -X DELETE http://localhost:5000/remove-container \
     -H "Content-Type: application/json" \
     -d '{"team_id": 2, "challenge_id": "nginx"}'
```

3. **List Active Containers**:

```
GET http://localhost:5000/active-containers
```

## Video

[Video](https://iutbox.iut.ac.ir/index.php/s/tb77Gk47WfzKpWk)
