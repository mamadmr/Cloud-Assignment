from celery import shared_task
import docker
from .models import Team, Challenge, Container
import os


@shared_task
def start_container_task(team_id, challenge_id):
    client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
    try:
        team = Team.objects.get(id=team_id)
        challenge = Challenge.objects.get(id=challenge_id)
        port = "3000/tcp" if challenge.challenge_id == "juice" else "8080/tcp"
        container = client.containers.run(
            challenge.image,
            detach=True,
            ports={port: None},  # Map host port dynamically
            network="ctf_network",
        )
        container.reload()
        ports = container.ports.get(port)
        if ports and len(ports) > 0:
            host_port = ports[0]["HostPort"]
            address = f"http://{container.attrs['NetworkSettings']['Networks']['ctf_network']['IPAddress']}:{host_port}"
        else:
            # Fallback if port mapping fails
            address = f"http://{container.attrs['NetworkSettings']['Networks']['ctf_network']['IPAddress']}:80"  # Default port
            host_port = "80"
        Container.objects.create(
            team=team, challenge=challenge, container_id=container.id, address=address
        )
        return {
            "status": "success",
            "container_id": container.id,
            "address": address,
            "host_port": host_port,
        }
    except docker.errors.DockerException as e:
        return {"status": "error", "message": f"Docker error: {str(e)}"}
    except (Team.DoesNotExist, Challenge.DoesNotExist) as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@shared_task
def stop_container_task(container_id):
    client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
    try:
        container = Container.objects.get(id=container_id)
        docker_container = client.containers.get(container.container_id)
        docker_container.stop()
        docker_container.remove()
        container.delete()
        return {"status": "success"}
    except docker.errors.DockerException as e:
        return {"status": "error", "message": f"Docker error: {str(e)}"}
    except Container.DoesNotExist:
        return {"status": "error", "message": "Container not found in database"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}
