The command below to create a container for redis in Docker
docker run --name my-redis -p 6379:6379 -d redis

-p 6379:6379: Maps port 6379 on the host to port 6379 in the container, allowing external access to Redis.
-d: Runs the container in detached mode (in the background).

We also use this command to install the Redis Python client:
pip install redis

Then we use 2 python scripts (publisher.py and subscribe.py) to send and receive messages using redis channel messages and transfer data with storing and querying data.

