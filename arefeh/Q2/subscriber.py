import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Retrieve key-values
print("team1:", r.get("team1"))
print("team2:", r.get("team2"))

# Subscribe to channel
pubsub = r.pubsub()
pubsub.subscribe("updates")
print("Subscribed to 'updates' channel")

# Listen for messages
for message in pubsub.listen():
    if message['type'] == 'message':
        print("Received:", message['data'])
