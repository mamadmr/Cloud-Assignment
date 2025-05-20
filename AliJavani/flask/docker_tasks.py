#docker_tasks.py
import docker
from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from models import SessionLocal, Container

app = Celery('docker_tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
client = docker.from_env()

@app.task
def start_container(team_id, challenge_id, image_name):
    try:
        container = client.containers.run(image_name, detach=True, ports={'80/tcp': None})
        address = container.attrs['NetworkSettings']['IPAddress']
        db = SessionLocal()
        new = Container(team_id=team_id, challenge_id=challenge_id, container_id=container.id, address=address)
        db.add(new)
        db.commit()
        db.close()
        return f"Started: {container.id} at {address}"
    except Exception as e:
        return f"Start failed: {str(e)}"

@app.task
def stop_container(team_id, challenge_id):
    db = SessionLocal()
    container = db.query(Container).filter_by(team_id=team_id, challenge_id=challenge_id).first()
    if not container:
        return "No such container"
    try:
        cont = client.containers.get(container.container_id)
        cont.stop()
        cont.remove()
        db.delete(container)
        db.commit()
        return f"Stopped and removed: {container.container_id}"
    except Exception as e:
        return f"Stop failed: {str(e)}"
    finally:
        db.close()
