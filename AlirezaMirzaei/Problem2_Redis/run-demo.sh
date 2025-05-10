#!/bin/bash

echo "Ensuring Redis is running..."
docker ps | grep redis-server > /dev/null
if [ $? -ne 0 ]; then
    echo "Redis server not running. Starting it now..."
    ./setup-redis.sh
fi

# Run the consumer in background
echo "Starting Redis consumer in background..."
./redis-consumer.py > consumer.log 2>&1 &
CONSUMER_PID=$!

echo "Consumer started with PID $CONSUMER_PID"
echo "Consumer logs are being written to consumer.log"

# Wait a bit to ensure consumer is ready
sleep 2

echo "Starting Redis producer in foreground..."
echo "Press Ctrl+C to stop the producer when done"
./redis-producer.py

# When producer is stopped, also stop the consumer
echo "Stopping consumer process..."
kill $CONSUMER_PID

echo "Demo completed. You can view the consumer logs in consumer.log"
