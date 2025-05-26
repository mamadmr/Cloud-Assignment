import redis

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Retrieve and display key-value pairs
keys = ["team:red", "team:blue"]
for key in keys:
    value = r.get(key)
    print(f"The value of '{key}' is: {value}")

# Subscribe to the channel
channel = "ctf_channel"
pubsub = r.pubsub()
pubsub.subscribe(channel)
print(f"Subscribed to {channel}. Waiting for messages...")

# Listen for messages
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received message on {channel}: {message['data']}")