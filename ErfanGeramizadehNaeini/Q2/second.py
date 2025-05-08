import redis
CHANNEL = 'erfangchannel'

r = redis.Redis(host='localhost', port=6390, decode_responses=True)
keys = r.keys('*')
print(keys)
for key in keys:
    value = r.get(key)
    print(f"{key}: {value}")

pubsub = r.pubsub()

pubsub.subscribe(CHANNEL)
print("Subscribed to 'mychannel'...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")
