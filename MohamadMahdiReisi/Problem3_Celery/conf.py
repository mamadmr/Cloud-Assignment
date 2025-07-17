import os
import docker
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = Celery('container_management',
             broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
             broker_connection_retry_on_startup=True)

client = docker.from_env()

DEFAULT_IMAGE = os.getenv('DEFAULT_IMAGE', 'docker.arvancloud.ir/postgres:latest')
MAX_CONTAINERS = int(os.getenv('MAX_CONTAINERS', '5'))

@app.task
def start_container(challenge_name):
    """Start a Docker container for a CTF challenge with safety checks"""
    try:
        print('chanllenge name is ', challenge_name)
        existing = client.containers.list(all=True)
        if len(existing) >= MAX_CONTAINERS:
            raise RuntimeError("Maximum container limit reached")

        container_config = {
            "image": DEFAULT_IMAGE,
            "environment": {"POSTGRES_PASSWORD": os.getenv('DB_PASSWORD', 'changeme')},
            "detach": True,
            "auto_remove": True,
            "network": os.getenv('NETWORK_NAME', 'ctf-network'),
            "mem_limit": os.getenv('MEM_LIMIT', '512m')
        }

        container = client.containers.run(
            name=f"ctf-{challenge_name}",
            **container_config
        )
        
        return {
            "status": "success",
            "container_id": container.id,
            "name": container.name
        }

    except docker.errors.DockerException as e:
        return {"status": "error", "message": f"Docker error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

@app.task
def stop_container(container_name):
    """Stop and clean up container with additional checks"""
    try:
        container = client.containers.get(container_name)
        if not container.name.startswith('ctf-'):
            raise PermissionError("Not authorized to stop non-CTF containers")
            
        container.stop()
        container.remove()
        return {"status": "success", "message": f"Removed {container_name}"}

    except docker.errors.NotFound:
        return {"status": "error", "message": "Container not found"}
    except docker.errors.APIError as e:
        return {"status": "error", "message": f"API error: {str(e)}"}