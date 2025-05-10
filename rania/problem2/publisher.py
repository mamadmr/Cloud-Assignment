import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('team1', 'Green Shoes')
r.set('team2', 'Red Hat')

for i in range(3):
    msg = f'Hello from publisher #{i}'
    r.publish('ctf-channel', msg)
    print('Published:', msg)
    time.sleep(1)

