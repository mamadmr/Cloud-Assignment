import redis
import time

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Set multiple key-value pairs
r.set("team:red", "assigned")
r.set("team:blue", "pending")
r.set("task:1", "in-progress")

print("Set key-value pairs: team:red=assigned, team:blue=pending, task:1=in-progress")

# Publish messages to a channel
channel = "task_updates"
for i in range(3):
    message = f"Task update {i+1}: Processing..."
    r.publish(channel, message)
    print(f"Published: {message}")
    time.sleep(1)
