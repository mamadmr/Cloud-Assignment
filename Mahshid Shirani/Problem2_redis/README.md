---

Section A: Deploy a Redis Server in Docker

1. Launch a Redis server container:

   docker run -d --name my\_redis -p 6379:6379 redis

2. The Redis server will now be running on localhost:6379 and accepting client connections.

---

Section B: Inter-Process Communication Using Redis

This section involves writing two Python programs that communicate with each other through Redis.

Program 1 (Publisher and Key Setter):

* Connects to Redis.
* Sets multiple key-value pairs.
* Publishes a series of messages to a Redis channel.

Python code (publisher.py):

import redis
import time

# Connect to Redis

r = redis.Redis(host='localhost', port=6379, decode\_responses=True)

# Set multiple key-value pairs

r.set('key1', 'value11')
r.set('key2', 'value22')
r.set('key3', 'value33')

print("Keys set. Now publishing messages...")

# Publish messages to a Redis channel

for i in range(150):
message = f"Hello from publisher {i}"
r.publish('my\_channel', message)
print(f"Published: {message}")
time.sleep(1)

# Final publish

r.publish('my\_channel', message)

Program 2 (Subscriber and Key Retriever):

* Connects to Redis.
* Retrieves and prints key-value pairs.
* Subscribes to the Redis channel and listens for published messages.

Python code (subscriber.py):

import redis

# Connect to Redis

r = redis.Redis(host='localhost', port=6379, decode\_responses=True)

# Retrieve and display key-value pairs

print("Retrieving keys:")
for key in \['key1', 'key2', 'key3']:
value = r.get(key)
print(f"{key}: {value}")

# Subscribe to the same channel

print("\nSubscribing to channel...\n")
pubsub = r.pubsub()
pubsub.subscribe('my\_channel')

for message in pubsub.listen():
if message\['type'] == 'message':
print(f"Received: {message\['data']}")

---
