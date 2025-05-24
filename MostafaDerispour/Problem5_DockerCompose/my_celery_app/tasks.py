import docker
import traceback
from my_celery_app.celery_app import app

client = docker.from_env()

@app.task
def start_container(team_id, challenge_id):
    image = "alpine" if challenge_id == 0 else "bkimminich/juice-shop"
    if not image:
        raise ValueError(f"No image defined for challenge_id {challenge_id}")
    
    container = client.containers.run(
        image=image,
        detach=True,
        name=f"{team_id}_{challenge_id}",
    )
    
    return {
        "container_id": container.id,
        "status": "started"
    }

@app.task
def stop_container(team_id, challenge_id):
    name = f"{team_id}_{challenge_id}"
    try:
        container = client.containers.get(name)
        container.stop()
        container.remove()
        return {"status": "stopped"}
    except docker.errors.NotFound:
        return {"status": "not found"}