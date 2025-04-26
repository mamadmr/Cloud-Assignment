# Problem 2: Redis Server Setup

This project sets up a Redis server and a real-time messaging system using Docker Compose and Python.

## Services

- **Redis**: A containerized Redis server.
- **RedisInsight**: A graphical interface for inspecting and managing Redis data.

## How to Use

To start the Redis server and RedisInsight UI, open your terminal in the project directory and run:

```bash
docker compose up --build
```

After the services are running:

- Access RedisInsight by visiting [http://localhost:5540](http://localhost:5540) in your web browser.
- Connect to the Redis server running at `localhost:6379`.

## Publisher and Subscriber Scripts

This project provides two simple Python scripts to interact with Redis:

- **publisher.py**:
  - Sets key-value pairs for team names and scores.
  - Publishes a message to a Redis channel (`ctf_channel`).

- **subscriber.py**:
  - Retrieves and displays the teams and their scores.
  - Subscribes to the `ctf_channel` and waits for new messages.

## How to Run the Scripts

First, install the required Python package:

```bash
pip install -r requirements.txt
```

Then, in two separate terminals:

- Run the subscriber:

```bash
python subscriber.py
```

- Run the publisher:

```bash
python publisher.py
```

You will see the subscriber receiving the published message and printing the updated information.

## Requirements

- Docker must be installed.
- Docker Compose must be installed.
- Python 3 must be installed.
- Port `6379` and `5540` must be available on your system.



