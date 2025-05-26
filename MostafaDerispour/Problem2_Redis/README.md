# Command Explainations

## Running Redis in Docker

To start a Redis server using Docker, use the following command:

```bash
sudo docker run --name my-redis -p 6379:6379 -d redis
```

* `sudo`: Runs Docker with superuser privileges.
* `docker run`: Launches a new Docker container.
* `--name my-redis`: Names the container `my-redis` so you can refer to it easily.
* `-p 6379:6379`: Maps port 6379 on your machine to port 6379 in the container (the default Redis port).
* `-d`: Runs the container in detached mode (in the background).
* `redis`: Uses the official Redis image from Docker Hub.

After running this command, your Redis server will be up and listening on `localhost:6379`.

---

## Setting Up the Python Environment

Before running the Python programs that communicate with Redis, you need to:

### 1. Create a Python Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

* On Linux/macOS:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---
# Videos Link
https://iutbox.iut.ac.ir/index.php/s/RpzHAzQbQcokCBL
