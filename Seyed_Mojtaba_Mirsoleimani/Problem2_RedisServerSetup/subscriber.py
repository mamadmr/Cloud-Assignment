import redis

redisObject = redis.Redis('localhost', 6379, 0)

pubsubObject = redisObject.pubsub()

pubsubObject.subscribe('DataFlow')

for data in pubsubObject.listen():
    print(f"{data}")