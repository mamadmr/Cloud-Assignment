import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Retrieve and display the key-value pairs
name = r.get('name').decode('utf-8')
language = r.get('language').decode('utf-8')
flag = r.get('flag').decode('utf-8')

print(f'Name: {name}')
print(f'Language: {language}')
print(f'Flag: {flag}')

# Subscribe to the Redis channel
def message_handler(message):
    print(f'Received message: {message["data"]}')

p = r.pubsub()
p.subscribe(**{'channel1': message_handler})

# Monitor the channel for messages
print('Waiting for messages...')
while True:
    p.get_message()
