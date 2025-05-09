import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()


pubsub.subscribe("team-updates")

print("Listening...")

for m in pubsub.listen():
    if m['type'] == 'message':
        if m['data'] == 'close':
            break

        data = m['data']
        key = data.split("/")[0]
        value = r.get(key)
        print(f"Subcription Message: {data}")
        print(f"Key/Value: {key}/{value}")
