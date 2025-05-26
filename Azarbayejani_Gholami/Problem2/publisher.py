
import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set key-value pairs
r.set("team:blue", "pending")
r.set("team:green", "assigned")

# Publish messages
for i in range(3):
    message = f"Task {i+1} dispatched"
    r.publish("ctf_channel", message)
    print(f"Published: {message}")
    time.sleep(1)

