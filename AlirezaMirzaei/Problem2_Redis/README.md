# My Redis Server & IPC Demo

We also need a lightweight pub/sub demo alongside Redis key/value storage, so here’s how I put that together for this assignment:

1. **Spinning up Redis**
   In `setup-redis.sh` I:
   - I made a folder for redis data (volume) to be mounted in.
   - I configured redis for listening address and mode of data access in `redis.conf`.
   - I start the container with image `6-alpine` with the given settings and options.
   - Check if redis is running successfuly using ping and pong command and output.
2. **Preparing my Python environment**
   I set up a virtualenv and installed `redis`:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install redis
   ```

3. **Writing the producer** (`redis-producer.py`)

   - Connect to Redis
   - Set a few string keys and a hash
   - Publish a “notification” every second, incrementing a counter

4. **Writing the consumer** (`redis-consumer.py`)

   - Connect to Redis
   - Dump all existing keys/hashes on start
   - Subscribe to the `notifications` channel and print each new message
   - The output is printed to stdout and can easily be inspected.

5. **Wrapping it all together**
   In `run-demo.sh` I made sure Redis is running, then:

   - I run the consumer file in background and set it's output to `consumer.log`.
   - I run the producer file in foreground and stop the consumer when the producer is stopped.
   - The logs can be viewed in `consumer.log`.

6. **Monitoring with RedisInsight**
   I used `setup-redisinsight.sh` to spin up RedisInsight so I could watch keys, hashes, and pub/sub traffic through a GUI.

7. **Wrap Up**
   The commands for using this module are run in this order:

   - `./setup-redis.sh` to run and install redis.
   - `./setup-redisinsight.sh` to run and install redis insight.
   - Install requirements as mentioned in step 2 (don't forget).
   - Run the demo file: `./run-demo.sh`.
   - Inspect the outputs and redis insight logs.

8. **To Restart**:
   - Run `docker stop redis-server` and `docker rm redis-server`.
   - Run the commands above again.

---

That’s exactly how I went step-by-step through each setup for this assignment—hope it’s clear and easy to follow from my perspective!
