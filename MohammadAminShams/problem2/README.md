# Problem 2: Setting up a Redis Server

This guide walks you through deploying a Redis server using Docker, creating Python programs to interact with it, and monitoring Redis activity using RedisInsight.

---

## Part (a): Running Redis in Docker

### 1. Pull and run Redis:

```bash
docker pull redis

docker network create   --subnet=172.20.0.0/16   custom

docker run -d   --name redis-ctf   -p 6379:6379   --network custom   --ip 172.20.1.3   redis:latest
```

### 2. Test the Redis connection:

```bash
docker ps

docker exec -it redis-ctf redis-cli
```

Inside `redis-cli`:

```bash
PING
```

Expected Output: `PONG`

---

## Part (b): Inter-process Communication using Redis

### 1. Install Redis Python library:

```bash
pip install redis
```

### 2. Create `producer.py`:

```python
import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("team:red", "assigned")
r.set("team:blue", "not_assigned")
print("Set key-value pairs: team:red=assigned, team:blue=not_assigned")

channel = "ctf_channel"
messages = ["Challenge 1 started", "Challenge 2 started", "Challenge 3 started"]
for msg in messages:
    r.publish(channel, msg)
    print(f"Published to {channel}: {msg}")
    time.sleep(1)
```

### 3. Create `consumer.py`:

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

keys = ["team:red", "team:blue"]
for key in keys:
    value = r.get(key)
    print(f"The value of '{key}' is: {value}")

channel = "ctf_channel"
pubsub = r.pubsub()
pubsub.subscribe(channel)
print(f"Subscribed to {channel}. Waiting for messages...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received message on {channel}: {message['data']}")
```

### 4. Run the programs:

First run the consumer:

```bash
python consumer.py
```

Then run the producer:

```bash
python producer.py
```

---

## Part (c): Monitor Redis with RedisInsight

### 1. Run RedisInsight via Docker:

```bash
docker run -d   --name redisinsight   -p 5540:5540   --network custom   --ip 172.20.1.4   redislabs/redisinsight:latest
```

### 2. Access the Web UI:

Open in your browser:

```
http://localhost:5540
```

Click **Add Redis Database** and fill in:

- Host: `host.docker.internal` or `localhost`
- Port: `6379`
- Name: `redis-ctf`

### 3. Monitor keys and messages:

- In **Browser**, view keys `team:red` and `team:blue`.
- In **Pub/Sub**, subscribe to `ctf_channel` and observe messages.

---

## Optional: Simple Test

Create `test_redis.py`:

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("team:red", "assigned")
value = r.get("team:red")
print(f"The value of 'team:red' is: {value}")
```

Run the test:

```bash
python test_redis.py
```

Expected output:

```
The value of 'team:red' is: assigned
```

---

End of Guide ✅