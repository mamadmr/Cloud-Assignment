from celery import Celery
import docker
from db import SessionLocal
from models import ContainerInfo

app = Celery(
	'tasks',
	broker='redis://redis:6379/0',
	backend='redis://redis:6379/0'
)

@app.task
def assign_container_task(team_id, challenge_id):
    session = SessionLocal()
    try:
        client = docker.from_env()
        image_name = f"ctf_challenge_{challenge_id}".strip()
        container_name = f"{team_id}_container".strip()

        # Remove existing container if exists
        try:
            existing = client.containers.get(container_name)
            existing.stop()
            existing.remove()
        except docker.errors.NotFound:
            pass

        container = client.containers.run(
            image=image_name,
            name=container_name,
            detach=True,
            ports={'80/tcp': None}
        )

        # Save to DB
        container_info = ContainerInfo(
            team_id=team_id,
            challenge_id=challenge_id,
            container_id=container.id
        )
        session.merge(container_info)
        session.commit()

        return {"status": "success", "container_id": container.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

@app.task
def remove_container_task(team_id, challenge_id):
    session = SessionLocal()
    try:
        client = docker.from_env()
        container_name = f"{team_id}_container".strip()

        # Remove container
        try:
            container = client.containers.get(container_name)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            pass

        # Remove DB entry
        obj = session.query(ContainerInfo).filter_by(team_id=team_id, challenge_id=challenge_id).first()
        if obj:
            session.delete(obj)
            session.commit()
            return {"status": "success", "message": f"Removed container {container_name}"}
        else:
            return {"status": "error", "message": "Entry not found in database"}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()
