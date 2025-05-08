## celery
The docker compose will bring uo the redis as well as celery 
I useed this bind mount so I can run docker containers outside of the existing container
- /var/run/docker.sock:/var/run/docker.sock

Celery depends on redis. It means that runing celery container depends on running redis container.
I used CELERY_BROKER_URL  and CELERY_RESULT_BACKEND for telling where to look for broker and backend(used in the tasks.py)
tasks.py defines some tasks that can be executed by calling send)task which is demonstrated in test.py

