from celery_app import celery_app
import docker
import os
from app.database import SessionLocal
from app.models import TeamChallenge

docker_client = docker.from_env()


@celery_app.task(bind=True)
def start_challenge(self, team_id: int, challenge_id: int) -> dict:
    # select image based on challenge_id
    images = {1: "pasapples/apjctf-todo-java-app:latest", 2: "bkimminich/juice-shop"}
    image = images.get(challenge_id)
    if not image:
        raise ValueError(f"Unknown challenge {challenge_id}")

    container = docker_client.containers.run(image, detach=True, ports={"80/tcp": None})
    container.reload()

    network_settings = container.attrs["NetworkSettings"]
    ports = network_settings.get("Ports", {})

    host_port = None
    for pinfo in ports.values():
        if pinfo and isinstance(pinfo, list):
            host_port = pinfo[0].get("HostPort")
            break

    if not host_port:
        raise RuntimeError("Could not determine mapped host port for container.")

    ip = os.getenv(
        "DOCKER_HOST_IP", "localhost"
    )  # Use .env override or default to localhost
    addr = f"http://{ip}:{host_port}"
    db = SessionLocal()
    tc = TeamChallenge(
        team_id=team_id,
        challenge_id=challenge_id,
        container_id=container.id,
        address=addr,
        status="running",
    )
    db.add(tc)
    db.commit()
    db.refresh(tc)
    db.close()

    return {
        "team_id": team_id,
        "challenge_id": challenge_id,
        "container_id": container.id,
        "address": addr,
        "status": "running",
    }


@celery_app.task(bind=True)
def stop_challenge(self, team_id: int, challenge_id: int) -> dict:
    db = SessionLocal()
    tc = (
        db.query(TeamChallenge)
        .filter_by(team_id=team_id, challenge_id=challenge_id, status="running")
        .first()
    )
    if not tc:
        raise ValueError(
            f"No active container for team {team_id} challenge {challenge_id}"
        )

    container = docker_client.containers.get(tc.container_id)
    container.stop()
    container.remove()
    tc.status = "stopped"
    db.commit()
    db.refresh(tc)
    db.close()

    return {
        "team_id": team_id,
        "challenge_id": challenge_id,
        "container_id": tc.container_id,
        "status": "stopped",
    }
