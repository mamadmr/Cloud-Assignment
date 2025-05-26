from celery import Celery
import docker

celery = Celery(
    'ctf_tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

client = docker.from_env()

@celery.task(name="start_ctf_container")
def start_ctf_container(team_id, challenge_id):
    image_map = {
        "juice_shop": "bkimminich/juice-shop",
        "todo_app": "pasapples/apjctf-todo-java-app"
    }
    image = image_map.get(challenge_id)
    if not image:
        raise Exception("Invalid challenge_id")

    container = client.containers.run(
        image,
        detach=True,
        name=f"{challenge_id}_{team_id}",
        network="ctf-net",
        ports={"3000/tcp": None}
    )

    port = 7352
    return {"container_id": container.id, "url": f"http://localhost:{port}"}

@celery.task(name="stop_ctf_container")
def stop_ctf_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
    return {"status": "removed"}
