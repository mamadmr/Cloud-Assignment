import logging

from docker import from_env as docker_from_env
from docker.errors import DockerException, NotFound

from celery import Celery

logger = logging.getLogger(__name__)

app = Celery('manage_ctf_docker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

app.conf.update(
    task_acks_late=True,
    worker_max_retries=3,
)

# A helper function to make sure that the connection to client is successful
def get_docker_client():
    try:
        return docker_from_env()
    except DockerException:
        logger.exception("Couldn't connect to docker client.")
        raise


@app.task
def start_ctf_docker():
    docker_cilent = get_docker_client()
    image_name = 'bkimminich/juice-shop'

    try:
        docker_cilent.images.pull(image_name)

        container = docker_cilent.containers.run(
            image_name,
            name="ctf_container",
            detach=True
        )

        logger.info("Started ctf container...")

        return container.id
    except DockerException as exc:
        logging.error("Faced an exception while trying to start ctf container")


@app.task
def stop_ctf_docker(container_id):
    docker_client = get_docker_client()

    try:
        container = docker_client.containers.get(container_id)

        container.stop()

        container.remove()

        logging.info("Stopped and removed ctf container")

        return True
    except NotFound:
        logging.error(f"Couldn't find the container with {container_id} id.")

        return False
    except DockerException as exc:
        logging.error("Faced an exception while trying to start ctf container")


