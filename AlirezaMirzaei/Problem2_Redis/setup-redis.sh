#!/bin/bash

# Create a directory for Redis data
mkdir -p redis-data

# Create a simple Redis configuration file for our needs
cat >redis.conf <<EOL
bind 0.0.0.0
port 6379
appendonly yes
protected-mode no
EOL

echo "Starting Redis container..."
docker run -d \
    --name redis-server \
    -p 6379:6379 \
    -v "$(pwd)/redis.conf:/usr/local/etc/redis/redis.conf" \
    -v "$(pwd)/redis-data:/data" \
    redis:6-alpine \
    redis-server /usr/local/etc/redis/redis.conf

echo "Waiting for Redis to start..."
sleep 2

# Test in a loop if Redis is working
echo "Waiting for Redis…"
until docker exec redis-server redis-cli PING | grep -q PONG; do
    sleep 1
done

if [ $? -eq 0 ]; then
    echo "Redis server is running successfully!"
else
    echo "Failed to start Redis server. Please check the logs:"
    docker logs redis-server
fi
