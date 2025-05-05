import redis
import time

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set multiple key-value pairs
r.set("team:red", "assigned")
r.set("team:blue", "not_assigned")
print("Set key-value pairs: team:red=assigned, team:blue=not_assigned")

# Publish messages to a channel
channel = "ctf_channel"
messages = ["Challenge 1 started", "Challenge 2 started", "Challenge 3 started"]
for msg in messages:
    r.publish(channel, msg)
    print(f"Published to {channel}: {msg}")
    time.sleep(1)  # Delay for clarity