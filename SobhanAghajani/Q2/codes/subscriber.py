import redis

client = redis.StrictRedis(host='localhost', port=6379, db=0)

print('key1:', client.get('key1').decode('utf-8'))
print('key2:', client.get('key2').decode('utf-8'))
print('key3:', client.get('key3').decode('utf-8'))

pubsub = client.pubsub()
pubsub.subscribe('my_channel')

print('Waiting for messages...')

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f'Received message: {message["data"].decode("utf-8")}')
