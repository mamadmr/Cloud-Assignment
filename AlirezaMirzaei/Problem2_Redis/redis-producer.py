#!/usr/bin/env python3
import redis
import time
import sys


def main():
    print("Producer: Connecting to Redis server...")
    try:
        # Connect to Redis server
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        r.ping()  # Test connection
        print("Producer: Successfully connected to Redis server")
    except redis.ConnectionError as e:
        print(f"Producer: Failed to connect to Redis: {e}", file=sys.stderr)
        sys.exit(1)

    # Set some key-value pairs
    print("Producer: Setting key-value pairs...")
    r.set("service_status", "running")
    r.set("last_update", time.strftime("%Y-%m-%d %H:%M:%S"))
    r.set("message_count", "0")

    # Create a hash (dictionary)
    r.hset(
        "system_info",
        mapping={
            "hostname": "redis-test",
            "version": "1.0.0",
            "environment": "development",
        },
    )

    print("Producer: Key-value pairs set successfully")

    # Publish messages to a channel
    channel = "notifications"
    message_count = 0

    print(f"Producer: Starting to publish messages to channel '{channel}'")
    print("Producer: Press Ctrl+C to stop")

    try:
        while True:
            message_count += 1
            message = f"Message #{message_count} at {time.strftime('%H:%M:%S')}"
            r.publish(channel, message)
            r.set("message_count", str(message_count))
            print(f"Producer: Published: {message}")

            # Sleep for 2 seconds between messages
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nProducer: Stopping message publication")

    print("Producer: Done")


if __name__ == "__main__":
    main()
