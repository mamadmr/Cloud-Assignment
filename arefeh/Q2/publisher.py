import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set some key-value pairs
r.set("team1", "Alpha")
r.set("team2", "Beta")

# Publish a message
for i in range(3):
    message = f"Task {i+1} completed"
    r.publish("updates", message)
    print(f"Published: {message}")
    time.sleep(1)
