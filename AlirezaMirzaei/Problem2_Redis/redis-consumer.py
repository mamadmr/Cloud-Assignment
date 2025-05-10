#!/usr/bin/env python3
import redis
import sys
import threading
import time
import logging

# Configure logging to write everything to consumer.log
logging.basicConfig(
    filename="consumer.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)


def subscribe_to_channel(r, channel):
    """Subscribe to the specified Redis channel and log messages"""
    logging.info(f"Subscribing to channel '{channel}'...")
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"]
            logging.info(f"Received message on '{channel}': {data}")


def fetch_data(r):
    """Periodically fetch and log data from Redis"""
    while True:
        try:
            service_status = r.get("service_status")
            last_update = r.get("last_update")
            message_count = r.get("message_count")
            system_info = r.hgetall("system_info")

            logging.info("Current Redis Data:")
            logging.info(f"  service_status: {service_status}")
            logging.info(f"  last_update:    {last_update}")
            logging.info(f"  message_count:  {message_count}")
            logging.info("  system_info:")
            for key, value in system_info.items():
                logging.info(f"    {key}: {value}")

            time.sleep(5)
        except Exception as e:
            logging.error(f"Error fetching data: {e}", exc_info=True)
            time.sleep(5)


def main():
    logging.info("Connecting to Redis server...")
    try:
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        r.ping()
        logging.info("Successfully connected to Redis server")
    except redis.ConnectionError as e:
        logging.error(f"Failed to connect to Redis: {e}")
        sys.exit(1)

    # Start data-fetch thread
    data_thread = threading.Thread(target=fetch_data, args=(r,), daemon=True)
    data_thread.start()

    # Run subscriber in main thread
    try:
        subscribe_to_channel(r, "notifications")
    except KeyboardInterrupt:
        logging.info("Shutting down consumer due to keyboard interrupt")

    logging.info("Consumer exiting")


if __name__ == "__main__":
    main()
