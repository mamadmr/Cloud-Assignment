import redis

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Set multiple key-value pairs
r.set("team:red", "red")
r.set("team:blue", "blue")

# Publish messages to a Redis channel
r.publish("channel1", "Hello from Program 1!")
print("Messages published and keys set.")
