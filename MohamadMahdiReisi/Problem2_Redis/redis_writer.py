import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("amir", "healthy")
r.set("ali", "sick")
r.set("reza", "dead")

print("Set key-value pairs")

channel = "task_updates"
for i in range(3):
    message = f"Task update {i+1}: Processing..."
    r.publish(channel, message)
    print(f"Published: {message}")
    time.sleep(1)