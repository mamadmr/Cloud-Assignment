# Redis Server Setup with Docker & Python

> This project demonstrates how to:
> 1. Run a Redis server inside Docker.  
> 2. Exchange messages via two Python programs (Publisher & Subscriber).  
> 3. Monitor Redis activity in real time using a GUI tool (e.g., RedisInsight).  
> 4. Document your setup and record a short demo video.

---

## Table of Contents

- [Prerequisites](#prerequisites)  
- [Building the Docker Image](#building-the-docker-image)  
- [Creating a Volume & Running the Container](#creating-a-volume--running-the-container)  
- [Project Structure](#project-structure)  
- [Usage](#usage)  
  - [Verifying Redis Is Running](#verifying-redis-is-running)  
  - [Running Publisher & Subscriber](#running-publisher--subscriber)  
- [Monitoring with RedisInsight](#monitoring-with-redisinsight)  
- [Recording a Short Demo Video](#recording-a-short-demo-video)  
- [License](#license)  

---

## Prerequisites

- Docker (version 20.10 or later)  
- Python 3.9+  
- Internet access to pull base images  
- (Optional) [RedisInsight](https://redis.com/redis-enterprise/redis-insight/) for GUI monitoring  

---

## Building the Docker Image

1. Open a terminal and navigate to the project root:
   ```bash
   cd /path/to/your/project

2. Build the Docker image:

   ```bash
   docker build -t redis_setup:latest .
   ```

---

## Creating a Volume & Running the Container

1. Create a Docker volume to persist Redis data:

   ```bash
   docker volume create redis_volume
   ```
2. Run the container in detached mode:

   ```bash
   docker run -d \
     --name redis_server_setup \
     -v redis_volume:/data \
     redis_setup:latest
   ```

---

## Project Structure

* **Dockerfile**

  * Base image: `python:3.9-slim`
  * Installs `redis-server` and Python `redis` package
  * Copies all project files into `/app`

* **entrypoint.sh**

  1. Starts Redis with `--appendonly yes` and stores data in `/data` (the mounted volume)
  2. Launches `subscriber.py` in the background
  3. After a short pause, runs `publisher.py`
  4. Waits for all processes to finish

* **publisher.py**

  * Connects to Redis at `localhost:6379`
  * Prepares a Python dict, serializes it to JSON
  * Publishes the JSON payload to channel `DataFlow`

* **subscriber.py**

  * Connects to the same Redis instance
  * Subscribes to `DataFlow` channel
  * Listens for messages and prints each one

---

## Usage

### Verifying Redis Is Running

Execute a quick ping to ensure Redis is up:

```bash
docker exec -it redis_server_setup redis-cli PING
# Expected output: PONG
```

### Running Publisher & Subscriber

Since `entrypoint.sh` launches both scripts automatically, you can follow their output via container logs:

```bash
docker logs -f redis_server_setup
```

* **Subscriber** will print a subscription confirmation:

  ```
  {'type': 'subscribe', 'pattern': None, 'channel': b'DataFlow', 'data': 1}
  ```
* **Publisher** will then publish the JSON message to the same channel.

---

## Monitoring with RedisInsight

1. Launch RedisInsight and create a new connection to `localhost:6379`.
2. Navigate to the **Browser** or **Pub/Sub Monitor** view.
3. Trigger the publisher/subscriber flow and watch messages appear in real time.
4. Example screenshots:

   ![RedisInsight Browser](./screenshots/redisinsight_browser.png)
   ![Pub/Sub Monitor](./screenshots/redisinsight_pubsub.png)

---

```
```
