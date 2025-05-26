import redis
import time
CHANNEL = 'erfangchannel'
r = redis.Redis(host='localhost', port=6390, decode_responses=True)


for i in range(5):
    r.set(f"hello{i}", f"world{i}")
i = 1
while (1):
    message = f"Hello {i}"
    r.publish(CHANNEL, message)
    print(f"Published: {message}")
    time.sleep(1)
    i += 1
