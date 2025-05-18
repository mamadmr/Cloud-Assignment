import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Get key-value pairs
print('Stored Key-Value Pairs:')
for key in ['name', 'age', 'country']:
    value = r.get(key)
    print(f'{key}: {value}')

# Subscribe to channel
print('\nListening for messages on "mychannel"...')
pubsub = r.pubsub()
pubsub.subscribe('mychannel')

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f'Received: {message["data"]}')
