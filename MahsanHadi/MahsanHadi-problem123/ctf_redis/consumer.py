import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# recieve key values
for key in ['Mahsan', 'Arman']:
    value = r.get(key)
    if value:
        print(f"{key}: {value}")
    else:
        print(f"{key}: key not found.")

# subscribe redis channel
channel = 'notifications'
pubsub = r.pubsub()
pubsub.subscribe(channel)

print("Consumer: Waiting for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received message: {message['data']}")
        break
        