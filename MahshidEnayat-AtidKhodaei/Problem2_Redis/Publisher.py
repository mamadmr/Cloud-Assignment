import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set key-value pairs
r.set("team:pink", "unassigned")
print("Data set.")
time.sleep(5)

# Publish message
for i in range(3):
    r.publish('channel1', f'Hello from publisher {i}')
    time.sleep(1)

print("Messages published.")
