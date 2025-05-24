import docker
from utils import app

client = docker.from_env()

@app.task
def start_ctf_container(image_name, container_name=None, ports=None):
    container = client.containers.run(
        image=image_name,
        name=container_name,
        detach=True,
        ports=ports or {},
        auto_remove=False
    )
    return {"status": "started", "container_id": container.id, "name": container.name}

@app.task
def stop_ctf_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    return {"status": "stopped", "container_id": container_id}

@app.task
def remove_ctf_container(container_id):
    container = client.containers.get(container_id)
    container.remove(force=True)  
    return {"status": "Removed", "container_id": container_id}

