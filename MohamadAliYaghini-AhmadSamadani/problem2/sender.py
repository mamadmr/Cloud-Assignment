import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("team:red", "assigned")
r.set("team:blue", "not_assigned")
print("Set key-value pairs: team:red=assigned, team:blue=not_assigned")

channel = "ctf_channel"
messages = ["Challenge 1 started", "Challenge 2 started", "Challenge 3 started", "Challenge 4 started", "Challenge 5 started"]

for msg in messages:
    r.publish(channel, msg)
    print(f"Send to {channel}: {msg}")
    time.sleep(1)
