import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Retrieve and display key-value pairs
keys = ['name', 'language', 'project']
for key in keys:
    value = r.get(key)
    print(f"{key}: {value}")

# Subscribe to Redis channel
pubsub = r.pubsub()
pubsub.subscribe('mychannel')
print("Subscribed to channel. Waiting for messages...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")
