import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set key-value pairs
r.set('name', 'Alice')
r.set('age', '30')
r.set('country', 'Wonderland')

# Publish messages
for i in range(3):
    message = f'Message {i + 2}'
    r.publish('mychannel', message)
    print(f'Published: {message}')
    time.sleep(1)
