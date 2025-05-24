1- Endpoint: api/add-user --> Create User(Team in this scenario)

2- Endpoint: api/start-container:

        Input structure:
                {
                        "user": "Team1",
                        "image_name": "pasapples/apjctf-todo-java-app:latest",
                        "container_name": "Q1",
                        "port": "9898"
                }

3- Endpoint api/stop-container -->

4- Endpoint api/remove-container -->

-------------------------------------------------------------------------------
Database Schema:
Table: container
----------------
id              : INTEGER (Auto-increment, Primary Key)
user_id         : INTEGER (One-to-One with auth_user.id, Unique, Not Null)
image_name      : VARCHAR(255) (Not Null)
container_name  : VARCHAR(255) (Not Null)
port            : INTEGER (Nullable)

Constraints:
- PRIMARY KEY (id)
- UNIQUE (user_id)
- FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE

-------------------------------------------------------------------------------
In Django Celery and Redis have no special configuration and they connect to each other via this simple code:
from celery import Celery

app = Celery('CTF',
            broker='redis://localhost:6379/0',  
            backend='redis://localhost:6379/0',
             include=['tasks'])  

--------------------------------------------------------------------------------
1- run a redis container : docker run --name my-rediss -p 6379:6379 -d docker.arvancloud.ir/redis:latest
2- run a celery worker : /account_app ->  celery -A utils.app worker --loglevel=info                                   
3- run django project : python3 manage.py runserver
4- Create User: http://127.0.0.1:8000/api/add-user/
5- from account_app/test/test.http send requests (We have used rest client extention (vscode) )

