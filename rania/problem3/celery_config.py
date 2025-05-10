import docker
from celery import Celery

# Create a Celery instance with Redis as the message broker
app = Celery('container_management', broker='redis://localhost:6379/0')

# Initialize the Docker client
client = docker.from_env()

@app.task
def start_container(container_name):
    """Start a Docker container for a specific CTF challenge."""
    try:
        # Use Docker SDK to run a container
        container = client.containers.run("docker.arvancloud.ir/postgres:latest",  # Docker image name
                                          name=container_name,   # Container name
                                          environment={"POSTGRES_PASSWORD":"1234"},
                                          detach=True,
                                          remove=False,
                                          )          # Run container in detached mode
        
        return f"Started container {container_name} with ID {container.id}"
    
    except docker.errors.ContainerError as e:
        return f"Error starting container: {str(e)}"
    except docker.errors.ImageNotFound as e:
        return f"Error: Docker image not found. {str(e)}"
    except Exception as e:
        return f"Failed to start container: {str(e)}"


@app.task
def stop_container(container_id):
    """Stop a running Docker container using its ID."""
    try:
        # Stop the Docker container by ID
        container = client.containers.get(container_id)
        container.stop()
        return f"Stopped container {container_id}"
    
    except docker.errors.NotFound as e:
        return f"Error: Container with ID {container_id} not found. {str(e)}"
    except Exception as e:
        return f"Failed to stop container: {str(e)}"
