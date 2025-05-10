import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("team:red", "assigned")


r.publish('updates', 'hello')
r.publish('updates', 'hello')
r.publish('updates', 'hello')
r.publish('updates', 'how low')

