import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

keys = ["amir", "ali", "reza"]
for key in keys:
    value = r.get(key)
    print(f"Key: {key}, Value: {value}")

pubsub = r.pubsub()
pubsub.subscribe("task_updates")
print("Subscribed to channel 'task_updates'. Waiting for messages...")

for message in pubsub.listen():
    if message["type"] == "message":
        print(f"Received: {message['data']}")