import docker
from celery_app2 import app
from celery import states
from celery.exceptions import Ignore

client = docker.from_env()

@app.task(bind=True)
def start_ctf_container(self, image_name, container_name=None):
    try:
        container = client.containers.run(
            image=image_name,
            name=container_name,
            detach=True
        )
        return {'container_id': container.id, 'status': 'started'}
    except Exception as e:
        self.update_state(state=states.FAILURE, meta={'exc': str(e)})
        raise Ignore()

@app.task(bind=True)
def stop_ctf_container(self, container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {'container_id': container.id, 'status': 'stopped'}
    except Exception as e:
        self.update_state(state=states.FAILURE, meta={'exc': str(e)})
        raise Ignore()
