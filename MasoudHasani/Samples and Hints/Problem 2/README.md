# Hint: Redis Key-Value Example in Python

This simple Python script shows how to connect to Redis, set a key-value pair, and retrieve it.

```python
import redis

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Set a key-value pair
r.set("team:red", "assigned")

# Get the value for the key
value = r.get("team:red")

print(f"The value of 'team:red' is: {value}")
```