
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Retrieve key-value pairs
print("team:blue =", r.get("team:blue"))
print("team:green =", r.get("team:green"))

# Subscribe to Redis channel
pubsub = r.pubsub()
pubsub.subscribe("ctf_channel")

print("Listening to messages on 'ctf_channel'...")

for message in pubsub.listen():
    if message["type"] == "message":
        print(f"Received: {message['data']}")

