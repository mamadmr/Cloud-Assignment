from celery import Celery
import docker

app = Celery('tasks',
    broker='redis://ctf_redis:6379/0',
    backend='redis://ctf_redis:6379/1'
)

docker_client = docker.from_env()

@app.task(bind=True)
def start_ctf(self, image_name: str, team_id: str, challenge: str) -> dict:
    name = f"{team_id}-{challenge}"
    try:
        old = docker_client.containers.get(name)
        old.stop(); old.remove()
    except docker.errors.NotFound:
        pass

    container = docker_client.containers.run(
        image_name, detach=True, name=name
    )
    address = f"http://{container.name}.local"
    return {'container_id': container.id, 'address': address}

@app.task(bind=True)
def stop_ctf(self, container_id: str) -> bool:
    
    try:
        cont = docker_client.containers.get(container_id)
        cont.stop(); cont.remove()
        return True
    except:
        return False
