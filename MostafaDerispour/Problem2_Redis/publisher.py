import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set key-value pairs
r.set('name', 'Redis')
r.set('language', 'Python')
r.set('project', 'IPC Example')

# Publish messages
for i in range(10):
    msg = f"Message {i}"
    r.publish('mychannel', msg)
    print(f"Published: {msg}")
    time.sleep(1)
