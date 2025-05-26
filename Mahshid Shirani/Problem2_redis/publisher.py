import redis
import time

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set multiple key-value pairs
r.set('key1', 'value11')
r.set('key2', 'value22')
r.set('key3', 'value33')

print("Keys set. Now publishing messages...")

# Publish messages to a Redis channel
for i in range(150):
    message = f"Hello from publisher {i}"
    r.publish('my_channel', message)
    print(f"Published: {message}")
    time.sleep(1)
r.publish('my_channel', message)
