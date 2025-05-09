import redis

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Retrieve and display key-value pairs
print("Retrieving keys:")
for key in ['key1', 'key2', 'key3']:
    value = r.get(key)
    print(f"{key}: {value}")

# Subscribe to the same channel
print("\nSubscribing to channel...\n")
pubsub = r.pubsub()
pubsub.subscribe('my_channel')

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")
