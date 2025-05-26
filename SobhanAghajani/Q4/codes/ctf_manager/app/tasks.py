from .celery_worker import celery
import docker
from .database import SessionLocal
from .models import Container

client = docker.from_env()

@celery.task
def start_container(team_id, challenge_id):
    sanitized_challenge_id = challenge_id.replace("/", "__")
    sanitized_challenge_id = sanitized_challenge_id.replace(":", "__")
    container_name = f"{team_id}_{sanitized_challenge_id}"
    try:
        container = client.containers.run(
            image=challenge_id,
            name=container_name,
            detach=True,
            ports={'3000/tcp': None, '80/tcp': None},
            restart_policy={"Name": "always"}
        )
        container.reload()
        ports = container.attrs['NetworkSettings']['Ports']
        host_port = None
        for port in ['3000/tcp', '80/tcp']:
            if ports.get(port) and ports[port][0].get('HostPort'):
                host_port = ports[port][0]['HostPort']
                break
        if not host_port:
            return {"error": "No host port exposed"}
        address = f"http://localhost:{host_port}"
        db = SessionLocal()
        db.add(Container(
            team_id=team_id,
            challenge_id=challenge_id,
            container_name=container_name,
            container_address=address
        ))
        db.commit()
        db.close()
        return {"container_address": address}
    except Exception as e:
        return {"error": str(e)}

@celery.task
def stop_container(team_id, challenge_id):
    db = SessionLocal()
    container = db.query(Container).filter_by(team_id=team_id, challenge_id=challenge_id).first()

    if container:
        docker_container = client.containers.get(container.container_name)
        docker_container.stop()
        docker_container.remove()

        container_id = container.container_address 

        db.delete(container)
        db.commit()
        db.close()
        return container_id  

    db.close()
    return None  


