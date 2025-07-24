from celery import Celery
import docker

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0' 
)

client = docker.from_env()

@celery_app.task
def start_container(image_name, team_id, challenge_id):
    container = client.containers.run(image_name, detach=True, ports={'80/tcp': None})
    container.reload()
    container_ip = container.attrs['NetworkSettings']['IPAddress']
    return {'container_id': container.id, 'container_address': container_ip}

@celery_app.task
def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
    return {'status': 'removed'}
