# Phase 4 and 5 - Web API and Docker-compose

### Step 1 - Run
Run the `docker-compose.yml' with this command to make everything up:
```
docker-compose up -d
```

### Step 2 - Database Schema
```
Database Schema
Table: container
----------------
id              : INTEGER (Auto-increment, Primary Key)
user_id         : INTEGER (One-to-One with auth_user.id, Unique, Not Null)
image_name      : VARCHAR(255) (Not Null)
container_name  : VARCHAR(255) (Not Null)

Constraints:
- PRIMARY KEY (id)
- UNIQUE (user_id)
- FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
```
### Step 3 - Celery & Redis
In Django Celery and Redis have no special configuration and they connect to each other via this simple code:

```
from celery import Celery

app = Celery('CTF',
            broker='redis://localhost:6379/0',  
            backend='redis://localhost:6379/0',
             include=['tasks'])  
```


### Step 4 - Endpoints

1- Endpoint: api/add-user --> Create User(Team in this scenario)

2- Endpoint: api/start-container:
```
{
    "user": "Example_team",
    "image_name": "pasapples/apjctf-todo-java-app:latest",
    "container_name": "Q1"
}
```
3- Endpoint api/stop-container:
```
{
    "user": "Example_team"
}
```

4- Endpoint api/remove-container:
```
{
    "user": "Example_team"
}
```



