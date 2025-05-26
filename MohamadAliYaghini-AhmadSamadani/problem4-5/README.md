# CTF Container Manager API

---

## Features

* Uses FastAPI to design a REST API
* Celery + Redis for background task processing
* PostgreSQL as the database
* Stores data only if the Celery task is successful
* Securely deletes containers
* Returns a unique address (IP/PORT) for each container

---

## Project Structure

```
project/
├── .env                    
├── Dockerfile              
├── docker-compose.yml      
├── requirements.txt        
└── app/
    ├── main.py             
    ├── tasks.py            
    ├── database.py         
    └── models.py           
```

---

## API Endpoints

### Create Container

```http
POST /create
```

Response:

```json
{
  "message": "Container is being created",
  "task_id": "...",
  "container_name": "ctf_container_ab12",
  "ip": "172.18.0.X",
  "port": 1337
}
```

---

### Delete Container

```http
DELETE /delete/{container_name}
```

Response:

```json
{ "message": "Container deleted successfully" }
```

---

### Check Task Status

```http
GET /task/{task_id}
```

Response:

```json
{
  "status": "SUCCESS",
  "result": {
    "ip": "172.18.0.X",
    "port": 1337
  }
}
```

