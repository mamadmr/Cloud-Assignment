from .celery_app import celery
from . import models, database
import docker
from sqlalchemy.orm import Session

client = docker.from_env()

@celery.task(name="start_container")
def start_container(image_name: str, ports: dict = None, team_id: str = None, challenge_id: str = None):
    try:
        container = client.containers.run(
            image_name,
            detach=True,
            ports=ports
        )
        container.reload()
        db = database.SessionLocal()
        port_number = None
        if ports:
            port_key = list(ports.keys())[0]
            mapped_ports = container.attrs['NetworkSettings']['Ports']
            if mapped_ports and port_key in mapped_ports and mapped_ports[port_key]:
                port_number = mapped_ports[port_key][0].get('HostPort')

        address = f"http://localhost:{port_number}" if port_number else ""

        
        db_container = models.Container(
            team_id=team_id,
            challenge_id=challenge_id,
            container_id=container.id,
            address=address
        )
        db.add(db_container)
        db.commit()
        db.close()
        return {"status": "success", "container_id": container.id, "address": address}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@celery.task(name="stop_container")
def stop_container(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        db = database.SessionLocal()
        db.query(models.Container).filter_by(container_id=container_id).delete()
        db.commit()
        db.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

