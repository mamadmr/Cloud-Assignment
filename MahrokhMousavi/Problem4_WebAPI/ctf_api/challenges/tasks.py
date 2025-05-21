from celery import shared_task
import docker
from .models import Team, Challenge, Container
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def start_container_task(team_id, challenge_id):
    client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
    try:
        team = Team.objects.get(team_id=team_id)
        challenge = Challenge.objects.get(challenge_id=challenge_id)

        # Validate port range
        if not (1 <= challenge.port <= 65535):
            raise ValueError(
                f"Invalid port for challenge {challenge.challenge_id}: {challenge.port}"
            )

        port = f"{challenge.port}/tcp"
        container = client.containers.run(
            challenge.image, detach=True, ports={port: None}, network="ctf_network"
        )

        # Retry to get host port mapping
        max_attempts = 5
        for attempt in range(max_attempts):
            container.reload()
            ports = container.ports.get(port)
            if ports and ports[0] and "HostPort" in ports[0]:
                host_port = ports[0]["HostPort"]
                address = f"http://localhost:{host_port}"
                break
            time.sleep(1)
        else:
            logger.error(
                f"Failed to get port mapping for {challenge.image} after {max_attempts} attempts"
            )
            container.stop()
            container.remove()
            raise RuntimeError("Could not determine host port mapping")

        container_obj = Container.objects.create(
            team=team,
            challenge=challenge,
            container_id=container.id,
            address=address,
        )
        logger.info(f"Container created: {container_obj}")
        return {
            "status": "success",
            "container_id": container.id,
            "address": address,
        }

    except docker.errors.DockerException as e:
        logger.error(f"Docker error: {e}")
        return {"status": "error", "message": str(e)}
    except (Team.DoesNotExist, Challenge.DoesNotExist, ValueError) as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"status": "error", "message": str(e)}


@shared_task
def stop_container_task(container_id):
    client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
    try:
        container = Container.objects.get(id=container_id)
        docker_container = client.containers.get(container.container_id)
        docker_container.stop()
        docker_container.remove()
        container.delete()
        logger.info(f"Container {container_id} stopped and removed")
        return {"status": "success"}

    except docker.errors.DockerException as e:
        logger.error(f"Docker error: {e}")
        return {"status": "error", "message": str(e)}
    except Container.DoesNotExist:
        logger.error("Container not found in database")
        return {"status": "error", "message": "Container not found in database"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"status": "error", "message": str(e)}
