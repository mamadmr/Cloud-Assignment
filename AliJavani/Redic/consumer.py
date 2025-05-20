import redis

r = redis.Redis(host='localhost', port=6379)


print("team1:", r.get('team1').decode())
print("team2:", r.get('team2').decode())

pubsub = r.pubsub()
pubsub.subscribe('ctf_channel')
print("Subscribed to channel...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print("Received message:", message['data'].decode())
