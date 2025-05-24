from celery_worker import celery_app
from docker import from_env
from database import SessionLocal, Container

client = from_env()

def get_container_name(team_id, challenge_id):
    return f"nginx_{team_id}_{challenge_id}"

@celery_app.task
def start_ctf_container(team_id: str, challenge_id: str):
    container = client.containers.run(
        image="nginx:latest",
        detach=True,
        name=get_container_name(team_id, challenge_id),
        ports={'80/tcp': None},  # random host port
        network_mode="bridge"
    )
    container.reload()
    host_port = container.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']

    db = SessionLocal()
    existing = db.query(Container).filter_by(team_id=team_id, challenge_id=challenge_id).first()
    if existing:
        existing.container_id = container.id
        existing.host_port = host_port
        existing.status = "active"
    else:
        db.add(Container(
            team_id=team_id,
            challenge_id=challenge_id,
            container_id=container.id,
            host_port=host_port,
            status="active"
        ))
    db.commit()
    db.close()
    return {"host_port": host_port}

@celery_app.task
def stop_ctf_container(team_id: str, challenge_id: str):
    db = SessionLocal()
    container_obj = db.query(Container).filter_by(team_id=team_id, challenge_id=challenge_id).first()

    if not container_obj:
        db.close()
        return {"error": "Container not found"}

    try:
        container = client.containers.get(container_obj.container_id)
        container.stop()
        container.remove()
        container_obj.status = "removed"
        db.commit()
    except Exception as e:
        db.close()
        return {"error": str(e)}

    db.close()
    return {"message": "Container stopped and removed"}
