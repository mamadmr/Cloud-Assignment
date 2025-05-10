import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

value = r.get("team:red")

print(f"The value of 'team:red' is: {value}")

pubsub = r.pubsub()
pubsub.subscribe('updates')

print("Listening for messages on 'updates' channel...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print("Received:", message['data'])

