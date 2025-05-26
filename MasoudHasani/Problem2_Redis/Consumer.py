import redis

# Connect to Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Retrive date
name = client.get('name').decode('utf-8')
age = client.get('age').decode('utf-8')
city = client.get('city').decode('utf-8')

print(f"Name: {name}, Age: {age}, City: {city}")

# Listening to channel
pubsub = client.pubsub()
pubsub.subscribe('my_channel')

print("Subscribed to the channel. Waiting for messages...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received message: {message['data'].decode('utf-8')}")
