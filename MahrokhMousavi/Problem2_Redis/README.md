
# Problem 2: Redis Server Setup

## 📌 Description

This part of the assignment demonstrates how to:

- Deploy a Redis server inside a Docker container.
- Use Redis as both a key-value store and a publish/subscribe message broker.
- Implement inter-process communication between two Python programs using Redis.
- Monitor Redis activity in real time using a GUI client like RedisInsight.

Redis is an open-source, in-memory data store known for high performance and support for various data structures.

---

## 🛠️ Steps to Run the Solution

### (a) Deploy a Redis Server in Docker

```bash
docker run -d --name my_redis -p 6379:6379 redis
````

#### 🔍 Explanation:

* `-d`: Runs the container in detached (background) mode.
* `--name my_redis`: Names the container.
* `-p 6379:6379`: Maps Redis’s default port from the container to your host.
* `redis`: Uses the official Redis image.

---

## 🧩 (b) Implement Inter-Process Communication Using Redis

Two Python scripts are used:

---

### ✅ `producer.py`

```python
import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set multiple key-value pairs
r.set("team:red", "assigned")
r.set("team:blue", "pending")
r.set("task:1", "in-progress")

print("Set key-value pairs: team:red=assigned, team:blue=pending, task:1=in-progress")

# Publish messages to a channel
channel = "task_updates"
for i in range(3):
    message = f"Task update {i+1}: Processing..."
    r.publish(channel, message)
    print(f"Published: {message}")
    time.sleep(1)
```

---

### ✅ `consumer.py`

```python
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Retrieve and display key-value pairs
keys = ["team:red", "team:blue", "task:1"]
for key in keys:
    value = r.get(key)
    print(f"Key: {key}, Value: {value}")

# Subscribe to the Redis channel
pubsub = r.pubsub()
pubsub.subscribe("task_updates")
print("Subscribed to channel 'task_updates'. Waiting for messages...")

# Listen for messages
for message in pubsub.listen():
    if message["type"] == "message":
        print(f"Received: {message['data']}")
```

---

## 📊 (c) Monitor Redis Activity Using RedisInsight

1. Download RedisInsight: [https://redis.com/redis-enterprise/redis-insight/](https://redis.com/redis-enterprise/redis-insight/)
2. Connect to:

   * **Host**: `localhost`
   * **Port**: `6379`
3. You’ll be able to:

   * View key-value pairs (`team:red`, `task:1`, etc.)
   * Monitor live messages on the `task_updates` channel

---

### 📷 Screenshot

![RedisInsight Screenshot]()

---

## 💡 Reasoning Behind Decisions

* **Dockerized Redis**: Simplifies setup and ensures isolation.
* **Separate producer/consumer scripts**: Clearly shows inter-process communication using Redis.
* **Pub/Sub channel (`task_updates`)**: Demonstrates real-time messaging.
* **RedisInsight**: Provides GUI-based verification and inspection.

---

## 🎥 Demonstration Video

📎 [Click here to view the video](https://iutbox.iut.ac.ir/your-upload-link)

> The video shows:
>
> * Running both Python scripts
> * Keys appearing in RedisInsight
> * Messages being published and received live

---
