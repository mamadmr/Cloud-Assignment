# Problem 2 – Redis In-Memory Data Store using Docker and Monitoring with RedisInsight

## Running Redis with Docker

To run Redis using Docker, the following command was used:

```bash
docker run --name redis_ctf -p 6379:6379 -d docker.arvancloud.ir/library/redis
````

* `--name redis_ctf`: Names the container `redis_ctf` for easier reference
* `-p 6379:6379`: Maps port `6379` of the host to the container, allowing applications to connect to Redis via `localhost:6379`
* `-d`: Runs the container in detached mode (in the background)
* `docker.arvancloud.ir/library/redis`: Uses the Redis image from ArvanCloud’s Docker registry (alternative to DockerHub due to access restrictions in Iran)

---

## Python Programs

### `publisher.py`

This script connects to the Redis server, sets key-value pairs representing challenge flags, and publishes update messages to a channel named `ctf_channel`.

```python
import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Store some flags
r.set("flag:challenge1", "CTF{easy_flag}")
r.set("flag:challenge2", "CTF{medium_flag}")
r.set("flag:challenge3", "CTF{hard_flag}")
print("Stored flags in Redis.")

# Publish messages
for i in range(3):
    message = f"Challenge {i+1} flag has been updated."
    r.publish("ctf_channel", message)
    print(f"Published: {message}")
    time.sleep(1)
```

---

### `subscriber.py`

This script retrieves the stored flags from Redis and subscribes to the `ctf_channel` to listen for messages in real time.

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Retrieve and print stored flag values
print("Stored Flags:")
for i in range(1, 4):
    key = f"flag:challenge{i}"
    value = r.get(key)
    print(f"{key} => {value}")

# Subscribe to channel
print("\nSubscribed to 'ctf_channel'. Waiting for messages...\n")
pubsub = r.pubsub()
pubsub.subscribe("ctf_channel")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"New message: {message['data']}")
```

---

## Monitoring Redis Using RedisInsight

To observe the state of Redis and see the data and messages in real time, I used the RedisInsight graphical tool.

1. I opened RedisInsight and connected to the Redis server running on `localhost:6379`.

2. After connecting, I explored different sections of RedisInsight:

   * In the **Browser** tab, I could view the keys I had previously stored using the Python script (like `flag:challenge1`, `flag:challenge2`, etc.) along with their values.
   * I also used the **Profiler** to monitor the commands executed by the Redis server (such as `SET`, `GET`, `PUBLISH`, etc.). This tool helped me better understand how the Python programs were interacting with Redis behind the scenes.

---

## Video and Screenshot

[Click here to view the video and screenshots](https://iutbox.iut.ac.ir/index.php/s/koWLQwss7qfsa4w)



