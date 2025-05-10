#!/usr/bin/env python3
"""
Celery tasks for managing Docker containers for CTF challenges
"""

import logging
import docker
from celery_app.celery_app import app

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Available CTF challenges per team
CTF_CHALLENGES = {
    "todo-app": {
        "image": "pasapples/apjctf-todo-java-app:latest",
        "ports": {"8080/tcp": ("0.0.0.0", 8080)},
        "environment": {"JAVA_OPTS": "-Xmx512m"},
    },
    "juice-shop": {
        "image": "bkimminich/juice-shop",
        "ports": {"3000/tcp": ("0.0.0.0", 3000)},
        "environment": {},
    },
}


@app.task(bind=True, name="tasks.start_container", max_retries=3)
def start_container(self, challenge_name, team_id):
    """
    Start a Docker container for a specific CTF challenge

    Args:
        challenge_name (str): Name of the challenge ('todo-app' or 'juice-shop')
        team_id (str): Unique identifier for the team

    Returns:
        dict: Container information including ID and status
    """
    try:
        if challenge_name not in CTF_CHALLENGES:
            error_msg = f"Unknown challenge: {challenge_name}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        # Initialize Docker client
        client = docker.from_env()

        # Get challenge configuration
        challenge = CTF_CHALLENGES[challenge_name]

        # Create container name with team_id to make it unique
        container_name = f"{challenge_name}-team-{team_id}"

        # Check if container with this name already exists
        existing_containers = client.containers.list(
            all=True, filters={"name": container_name}
        )
        if existing_containers:
            # If container exists, start it if it's not running
            container = existing_containers[0]
            if container.status != "running":
                logger.info(f"Starting existing container {container_name}")
                container.start()
            else:
                logger.info(f"Container {container_name} is already running")
        else:
            # Create and start new container
            logger.info(f"Creating new container for {challenge_name} (Team {team_id})")
            container = client.containers.run(
                image=challenge["image"],
                detach=True,
                name=container_name,
                ports=challenge["ports"],
                environment=challenge["environment"],
                restart_policy={"Name": "unless-stopped"},
            )

        # Get container info
        container.reload()
        container_info = {
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0]
            if container.image.tags
            else str(container.image.id),
            "ports": challenge["ports"],
        }

        logger.info(f"Container started successfully: {container_info}")
        return {"status": "success", "container": container_info}

    except docker.errors.APIError as e:
        logger.error(f"Docker API error: {str(e)}")
        # Retry with exponential backoff
        self.retry(exc=e, countdown=2**self.request.retries)
    except Exception as e:
        logger.error(f"Error starting container: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.task(bind=True, name="tasks.stop_container", max_retries=3)
def stop_container(self, container_id):
    """
    Stop a running Docker container

    Args:
        container_id (str): ID of the container to stop

    Returns:
        dict: Status information
    """
    try:
        # Initialize Docker client
        client = docker.from_env()

        # Try to get the container
        try:
            container = client.containers.get(container_id)
        except docker.errors.NotFound:
            error_msg = f"Container {container_id} not found"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        # Stop the container
        logger.info(f"Stopping container {container_id}")
        container.stop(timeout=10)  # Give it 10 seconds to gracefully stop

        # Verify container is stopped
        container.reload()

        result = {
            "status": "success",
            "container_id": container_id,
            "container_status": container.status,
            "message": f"Container {container_id} stopped successfully",
        }

        logger.info(result["message"])
        return result

    except docker.errors.APIError as e:
        logger.error(f"Docker API error: {str(e)}")
        # Retry with exponential backoff
        self.retry(exc=e, countdown=2**self.request.retries)
    except Exception as e:
        error_msg = f"Error stopping container: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}


@app.task(bind=True, name="tasks.get_container_status", max_retries=3)
def get_container_status(self, container_id=None, team_id=None, challenge_name=None):
    """
    Get status information for containers

    Args:
        container_id (str, optional): Specific container ID
        team_id (str, optional): Team ID to filter containers
        challenge_name (str, optional): Challenge name to filter containers

    Returns:
        dict: Container status information
    """
    try:
        # Initialize Docker client
        client = docker.from_env()

        # If container_id is provided, get specific container
        if container_id:
            try:
                container = client.containers.get(container_id)
                container.reload()
                return {
                    "status": "success",
                    "container": {
                        "id": container.id,
                        "name": container.name,
                        "status": container.status,
                        "image": container.image.tags[0]
                        if container.image.tags
                        else str(container.image.id),
                    },
                }
            except docker.errors.NotFound:
                return {
                    "status": "error",
                    "message": f"Container {container_id} not found",
                }

        # Otherwise get all containers matching filters
        filters = {}
        if team_id and challenge_name:
            filters["name"] = f"{challenge_name}-team-{team_id}"
        elif team_id:
            filters["name"] = f"team-{team_id}"
        elif challenge_name:
            filters["name"] = f"{challenge_name}"

        containers = client.containers.list(all=True, filters=filters)

        results = {
            "status": "success",
            "count": len(containers),
            "containers": [
                {
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0]
                    if container.image.tags
                    else str(container.image.id),
                }
                for container in containers
            ],
        }

        return results

    except docker.errors.APIError as e:
        logger.error(f"Docker API error: {str(e)}")
        # Retry with exponential backoff
        self.retry(exc=e, countdown=2**self.request.retries)
    except Exception as e:
        error_msg = f"Error getting container status: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}
