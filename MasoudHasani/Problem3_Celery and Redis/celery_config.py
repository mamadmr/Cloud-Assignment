from celery import Celery

app = Celery('docker_tasks', broker='pyamqp://guest@localhost//')

@app.task
def start_container(container_name):
    import docker
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.start()
    return f"Container {container_name} started."

@app.task
def stop_container(container_name):
    import docker
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.stop()
    return f"Container {container_name} stopped."
