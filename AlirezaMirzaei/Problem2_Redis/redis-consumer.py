#!/usr/bin/env python3
import redis
import sys
import threading
import time


def subscribe_to_channel(r, channel):
    """Subscribe to the specified Redis channel and print messages"""
    print(f"Consumer: Subscribing to channel '{channel}'...")
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    # Process messages
    print(f"Consumer: Listening for messages on channel '{channel}'...")
    for message in pubsub.listen():
        if message["type"] == "message":
            print(f"Consumer: Received message: {message['data']}")


def fetch_data(r):
    """Periodically fetch and display data from Redis"""
    while True:
        try:
            # Get simple key-value pairs
            service_status = r.get("service_status")
            last_update = r.get("last_update")
            message_count = r.get("message_count")

            # Get hash data
            system_info = r.hgetall("system_info")

            # Print the data
            print("\nConsumer: Current Redis Data:")
            print(f"  - service_status: {service_status}")
            print(f"  - last_update: {last_update}")
            print(f"  - message_count: {message_count}")
            print("  - system_info:")
            for key, value in system_info.items():
                print(f"      {key}: {value}")

            # Wait before polling again
            time.sleep(5)
        except Exception as e:
            print(f"Consumer: Error fetching data: {e}", file=sys.stderr)
            time.sleep(5)


def main():
    print("Consumer: Connecting to Redis server...")
    try:
        # Connect to Redis server
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        r.ping()  # Test connection
        print("Consumer: Successfully connected to Redis server")
    except redis.ConnectionError as e:
        print(f"Consumer: Failed to connect to Redis: {e}", file=sys.stderr)
        sys.exit(1)

    # Start a thread to fetch data periodically
    data_thread = threading.Thread(target=fetch_data, args=(r,), daemon=True)
    data_thread.start()

    # Subscribe to channel in the main thread
    try:
        subscribe_to_channel(r, "notifications")
    except KeyboardInterrupt:
        print("\nConsumer: Shutting down...")

    print("Consumer: Done")


if __name__ == "__main__":
    main()
