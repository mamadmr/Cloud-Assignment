from celery import Celery
import docker

app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1'
)

docker_client = docker.from_env()

@app.task(bind=True)
def start_ctf(self, image_name: str, team_id: str) -> str:
    try:
        name = f"{team_id}-{image_name}"
        try:
            existing = docker_client.containers.get(name)
            existing.stop()
            existing.remove()
        except docker.errors.NotFound:
            pass

        container = docker_client.containers.run(
            image_name,
            detach=True,
            name=name
        )
        return container.id
    except Exception as e:
        print("Error in start_ctf:", e)
        return None

@app.task(bind=True)
def stop_ctf(self, container_id: str) -> bool:
    try:
        container = docker_client.containers.get(container_id)
        container.stop()
        container.remove()
        print(f"Container {container_id} stopped and removed.")
        return True
    except Exception as e:
        print(f"Unexpected error in stop_ctf: {e}")
        return False
