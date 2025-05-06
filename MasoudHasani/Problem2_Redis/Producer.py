import redis
import time

# Connect to Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Adding key-value to redis
client.set('name', 'Alice')
client.set('age', 30)
client.set('city', 'New York')

print("Keys have been set in Redis.")

# Forward mail
while True:
    client.publish('my_channel', 'Hello from the producer!')
    print("Message sent to channel.")
    time.sleep(2)  
