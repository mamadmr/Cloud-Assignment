# Problem 2: Setting up a Redis Server

---

## a) Run Redis with container
---
### Step 1: run Redis and test connection:

```bash
docker run -d --name redis-ctf -p 6379:6379 redis
docker ps
docker exec -it redis-ctf redis-cli
```
---
## b) Implement Inter-Process Communication Using Redis
---
### Step 1: Install Redis library:

```bash
pip install redis
```
---
### Step 2: Create `sender.py`:

```python
import redis
import time

r = redis.Redis ( host='localhost', port=6379, decode_responses=True)
r.set("team:red", "assigned")
r.set("team:blue", "not_assigned")
print("Set key-value pairs: team:red=assigned, team:blue=not_assigned")

channel = "ctf_channel"
messages = ["Challenge 1 started", "Challenge 2 started", "Challenge 3 started", "Challenge 4 started", "Challenge 5 started"]

for msg in messages:
    r.publish(channel, msg)
    print(f"Send to {channel}: {msg}")
    time.sleep(1)
```
---
### Step 3: Create `receiver.py`:

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

---

### Step 4: Run python scripts.

---

## c) Monitor Redis with RedisInsight
---
### Step 1: Run RedisInsight via Docker:

```bash
docker run -d  --name redisinsight  -p 5540:5540  redislabs/redisinsight
```
---
### Step 2: Web UI:

```
http://localhost:5540
```

---

### Step 3: Monitor keys and messages:

- In **Browser**, view keys `team:red` and `team:blue`.
- In **Pub/Sub**, subscribe to `ctf_channel` and observe messages.

---
