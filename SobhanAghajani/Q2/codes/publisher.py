import redis

client = redis.StrictRedis(host='localhost', port=6379, db=0)

client.set('key1', 'value1')
client.set('key2', 'value2')
client.set('key3', 'value3')

client.publish('my_channel', 'Hello from the publisher!')
client.publish('my_channel', 'Another message!')
