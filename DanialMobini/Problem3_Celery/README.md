# Container Management with Celery and Redis

## (a)

```bash
pip install celery redis docker
```

### (i)

[celery_app](./celery_app.py)

### (ii)

```bash
docker run -d --name redis_server -p 6379:6379 my_redis_server
```

```bash
celery -A celery_app worker --loglevel=info
```

## (b)

### (i)

[task](./tasks.py)

#### (a)

```python
@app.task
def start_container(image_name):
    try:
        container = client.containers.run(image_name, detach=True)
        return f"Container started with ID: {container.id}"
    except Exception as e:
        return f"Error starting container: {str(e)}"
```

#### (b)

```python
@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Container with ID {container_id} stopped."
    except Exception as e:
        return f"Error stopping container: {str(e)}"
```

### (ii)

```python
# Start a container
result = start_container.delay("nginx:latest")
print(result.get())  # Wait for the task to complete and get the result

# Stop a container
result = stop_container.delay("<container_id>")
print(result.get())
```

## (c)

### (i)

```bash
docker run -d --name redis_server -p 6379:6379 my_redis_server

celery -A celery_app worker --loglevel=info
```

### (ii)

## (d)

### (ii)

[video](https://iutbox.iut.ac.ir/index.php/s/GynPzipkrozZWjD)
