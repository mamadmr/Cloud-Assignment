#!/bin/bash

echo "Setting up RedisInsight for monitoring Redis..."

# Pull and run RedisInsight container
docker run -d \
    --name redisinsight \
    -p 5540:5540 \
    -v redisinsight:/data \
    redislabs/redisinsight:latest

echo "RedisInsight is now running"
echo "Access it at: http://localhost:5540"
echo ""
echo "Instructions to connect to your Redis instance:"
echo "1. Open http://localhost:5540 in your browser"
echo "2. Click on 'Add Redis Database'"
echo "3. Enter the following details:"
echo "   - Host: host.docker.internal (if on Mac/Windows) or your Docker host IP"
echo "   - Port: 6379"
echo "   - Name: Redis-Server"
echo "4. Click 'Add Redis Database'"
echo ""
echo "You can now monitor your Redis keys, execute commands, and view real-time activity"
