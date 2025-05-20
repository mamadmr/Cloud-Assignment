# filepath: /path/to/second_program.py
import redis

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Retrieve and display key-value pairs
print("team:red:", r.get("team:red"))
print("team:blue:", r.get("team:blue"))

# Subscribe to the Redis channel
pubsub = r.pubsub()
pubsub.subscribe("channel1")

print("Subscribed to channel1. Waiting for messages...")
for message in pubsub.listen():
    if message["type"] == "message":
        print(f"Received message: {message['data']}")
