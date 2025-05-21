import redis

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

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
