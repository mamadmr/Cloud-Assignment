import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# make key values
r.set('Mahsan', 'Player1')
r.set('Arman', 'Player2')

# send message
channel = 'notifications'
r.publish(channel, 'start!')

print("Producer: sent messages.")
