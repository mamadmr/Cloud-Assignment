import docker
from datetime import datetime
from config.celery_setup import celery_app

client = docker.from_env()

class ContainerManager:
    def __init__(self):
        self.client = client

    def create_name(self, team, challenge):
        ts = datetime.now().strftime('%H%M%S')
        return f"{team}_{challenge}_{ts}"

@celery_app.task(name="ctf.start_task")
def start_container(team, challenge, image):
    manager = ContainerManager()
    container_name = manager.create_name(team, challenge)
    try:
        container = client.containers.run(
            image=image,
            name=container_name,
            detach=True,
            labels={"team": team, "challenge": challenge}
        )
        return {
            "status": "running",
            "name": container_name,
            "short_id": container.short_id
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@celery_app.task(name="ctf.stop_task")
def stop_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return {"status": "removed", "name": container_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}
