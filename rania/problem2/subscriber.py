import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print('team1 =>', r.get('team1'))
print('team2 =>', r.get('team2'))

pubsub = r.pubsub()
pubsub.subscribe('ctf-channel')
print('Subscribed to ctf-channel')

for message in pubsub.listen():
    if message['type'] == 'message':
        print('Received:', message['data'])

