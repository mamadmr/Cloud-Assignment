import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Set multiple key-value pairs
r.set('name', 'Redis')
r.set('language', 'Python')
r.set('flag', 'flag{this_is_a_flag}')


# Publish a message to a channel
r.publish('channel1', 'Hello from Redis!')