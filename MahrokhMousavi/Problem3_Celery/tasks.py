from celery import Celery
import docker

app = Celery('ctf_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
client = docker.from_env()

@app.task
def start_ctf_container(image_name, container_name):
    try:
        try:
            existing = client.containers.get(container_name)
            if existing.status == 'running':
                return f"Container {container_name} already running"
            existing.remove()
        except docker.errors.NotFound:
            pass
        
        container = client.containers.run(image_name, name=container_name, detach=True)
        return f"Started container: {container.id}"
    except Exception as e:
        return f"Error starting container: {str(e)}"

@app.task
def stop_ctf_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return f"Stopped and removed container: {container_id}"
    except docker.errors.NotFound:
        return f"Container {container_id} not found"
    except Exception as e:
        return f"Error stopping container: {str(e)}"
