# Redis Server Setup with Docker and Python Integration

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Redis Server Deployment](#redis-server-deployment)
- [Python Programs for Redis Operations](#python-programs-for-redis-operations)
- [Redis Monitoring](#redis-monitoring)
- [Demonstration](#demonstration)
- [Cleanup](#cleanup)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This solution demonstrates how to:
1. Deploy a Redis server in Docker
2. Implement Python programs for Redis operations
3. Monitor Redis activity using RedisInsight
4. Document the inter-process communication

## Prerequisites

- Docker installed
- Python 3.6+ with `redis-py` package (`pip install redis`)
- (Optional) RedisInsight for monitoring

## Redis Server Deployment

### 1. Launch Redis Container
```bash
docker run -d --name redis_server -p 6379:6379 redis:latest
```

### 2. Verify Connection
```bash
docker exec -it redis_server redis-cli ping
# Should respond with "PONG"
```

## Python Programs for Redis Operations

### Program 1: Redis Writer (`redis_writer.py`)
```python
import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)

# Set key-value pairs
r.set('server:name', 'Redis CTF Server')
r.set('server:uptime', '24 hours')
r.hset('user:1001', mapping={'name': 'Alice', 'score': '850'})

# Publish messages
for i in range(3):
    r.publish('ctf-channel', f'Message {i+1} from writer')
    time.sleep(1)
```

### Program 2: Redis Reader (`redis_reader.py`)
```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Retrieve key-value pairs
print("Key-Value Pairs:")
print(f"Server Name: {r.get('server:name').decode('utf-8')}")
print(f"Server Uptime: {r.get('server:uptime').decode('utf-8')}")
print(f"User Data: {r.hgetall('user:1001')}")

# Subscribe to channel
pubsub = r.pubsub()
pubsub.subscribe('ctf-channel')

print("\nWaiting for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data'].decode('utf-8')}")
```

### Running the Programs
1. First terminal:
```bash
python3 redis_writer.py
```

2. Second terminal:
```bash
python3 redis_reader.py
```

### Screenshot Checklist
**desierd output**
<img src="./../../shots/q2/Screenshot from 2025-05-12 01-45-19.png" width="400" alt="">
<img src="./../../shots/q2/Screenshot from 2025-05-12 01-45-47.png" width="400" alt="">

## Demonstration

### Video Script (30 seconds)
1. Show Redis container running (`docker ps`)
2. Execute `redis_writer.py` (terminal)
3. Execute `redis_reader.py` (terminal)
4. Show RedisInsight with real-time data
5. Stop container (`docker stop redis_server`)

## Cleanup

```bash
docker stop redis_server
docker rm redis_server
```

## License

MIT License - See [LICENSE](LICENSE) for details.