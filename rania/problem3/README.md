# **Setup process**
## Step 1
pip install celery
## Step 2
docker run --name redis-server -p 6379:6379 -d redis

<span style="color:green">run the redis server's container</span>
## Step 3
celery -A celery_config.app worker --loglevel=info

<span style="color:green">Creation of a Celery background worker for doing tasks that are in Redis</span>
## Step 4
run the start.py <myContainer> for start a task and run a specefied container <myContainer>
## Step 5
run stop.py for stop the container 

<span style="color:red">**(In our file we use a postgres image for test)**</span>

