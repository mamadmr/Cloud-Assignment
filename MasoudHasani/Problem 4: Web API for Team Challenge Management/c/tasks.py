# tasks.py
from celery import Celery
import docker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import ActiveContainer, Base, DATABASE_URL

app = Celery("ctf_tasks", broker="redis://localhost:6379/0")
docker_client = docker.from_env()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

@app.task
def assign_container_task(team_id, challenge_id):
    image_name = f"ctf_challenge_{challenge_id}"
    try:
        container = docker_client.containers.run(image_name, detach=True, ports={"80/tcp": None})
        container.reload()
        ip_address = container.attrs["NetworkSettings"]["IPAddress"]

        db = SessionLocal()
        new_container = ActiveContainer(
            team_id=team_id,
            challenge_id=challenge_id,
            container_id=container.id,
            container_address=ip_address
        )
        db.add(new_container)
        db.commit()
        db.close()

        return {"status": "success", "container_id": container.id, "container_address": ip_address}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.task
def remove_container_task(container_id):
    try:
        container = docker_client.containers.get(container_id)
        container.stop()
        container.remove()

        db = SessionLocal()
        record = db.query(ActiveContainer).filter_by(container_id=container_id).first()
        if record:
            db.delete(record)
            db.commit()
        db.close()

        return {"status": "success", "message": "Container removed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
