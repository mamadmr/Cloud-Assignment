import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Get key-value pairs
value = r.get('team:pink')    
print(f"The value of 'team:pink' is: {value}")

# Subscribe to the channel
pubsub = r.pubsub()
pubsub.subscribe('channel1')

print("Subscribed to channel1. Waiting for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")
