import docker
from mycelery import app
from celery import states
from celery.exceptions import Ignore

client = docker.from_env()



@app.task(bind=True)

def start_container(self, challenge_name, image_name, ports=None, env_vars=None):
    try:
        # deleting old containers with this name
        try:
            old_container = client.containers.get(challenge_name)
            old_container.stop()
            old_container.remove()
        except docker.errors.NotFound:
            pass

        # run new container
        container = client.containers.run(
            image_name,
            name=challenge_name,
            detach=True,
            ports=ports or {},
            environment=env_vars or {}
        )
        return {"status": "started", "container_id": container.id}
    except Exception as e:
        import traceback
        print("🔥 Exception while starting container:", traceback.format_exc())
        self.update_state(state=states.FAILURE, meta={
            'exc_type': type(e).__name__,
            'exc_message': str(e),
            'traceback': traceback.format_exc(),
        })
        raise Ignore()



@app.task(bind=True)
def stop_container(self, container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return {"status": "stopped", "container_id": container_id}
    except Exception as e:
        self.update_state(state=states.FAILURE, meta={
            'exc_type': type(e).__name__,
            'exc_message': str(e),
            'traceback': traceback.format_exc(),
        })
        raise Ignore()
