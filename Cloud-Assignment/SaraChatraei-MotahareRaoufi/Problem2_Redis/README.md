# Problem2: Redis

## 1. Redis Docker Deployment

I started by launching a Redis server in a Docker container using the official image. I exposed the default Redis port (6379) to my host so that I could interact with it both programmatically and through external tools like RedisInsight.
Command used:

```bash
docker run -d --name redis-server -p 6379:6379 redis
```

To verify the server was working correctly, I connected to it using the Redis CLI:

```bash
docker exec -it redis-server redis-cli
ping
```
The server responded with PONG, confirming a successful setup.

## 2. Python Programs for Inter-Process Communication

To demonstrate Redis messaging and key-value storage, I wrote two separate Python scripts:

### (a) sender.py
This script connects to the Redis server, sets multiple key-value pairs, and publishes a series of messages to a Redis channel called ctf_channel.

```python
import redis
import time
r = redis.Redis(host='localhost', port=6379, db=0)
# Set some key-value pairs
r.set('team1', 'Red')
r.set('team2', 'Blue')
# Publish messages to a channel
channel = 'ctf_channel'
for i in range(5):
    message = f"Flag update {i}"
    r.publish(channel, message)
    print(f"[Sender] Published: {message}")
    time.sleep(1)
```

### (b) receiver.py
This script retrieves the previously set key-value pairs and subscribes to the same Redis channel. It listens for incoming messages and displays them in real-time.

``` python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
# Retrieve and display keys
print("[Receiver] team1:", r.get('team1').decode())
print("[Receiver] team2:", r.get('team2').decode())
# Subscribe to channel
pubsub = r.pubsub()
pubsub.subscribe('ctf_channel')
print("[Receiver] Subscribed to ctf_channel...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"[Receiver] Received: {message['data'].decode()}")
```

Note: To observe communication properly, I ran receiver.py first and then sender.py in another terminal.


## 3. Redis Monitoring with RedisInsight

To visually monitor Redis data and messaging activity, I used RedisInsight. I connected to localhost:6379, and in the GUI, I could:
    View the team1 and team2 keys in the Browser tab.
    Monitor messages published to ctf_channel in the Pub/Sub tab in real-time.
This gave me a clearer picture of how Redis is handling background tasks and live data flows.


## Video report available at https://iutbox.iut.ac.ir/index.php/s/jWeXYoimcZCaRfN