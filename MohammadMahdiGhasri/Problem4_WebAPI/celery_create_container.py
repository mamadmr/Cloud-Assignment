from celery_docker_ctf import start_container, generate_container_name
import docker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Docker client
docker_client = docker.from_env()

def demonstrate_create_task():
    """
    Demonstrate task execution to start a container with unique name, IP, and port.
    """
    container_name = generate_container_name()
    image_name = "nginx:latest"
    
    try:
        logger.info(f"Initiating container start task for {container_name}...")
        start_result = start_container.delay(image_name, container_name)
        start_result.wait()
        
        if start_result.successful():
            result = start_result.get()
            logger.info(f"Start task result: {result}")
            container_id = result.get('container_id')
            
            if container_id:
                container = docker_client.containers.get(container_id)
                logger.info(f"Container status after start: {container.status}")
                logger.info(f"Container IP: {result.get('ip_address')}, Host Port: {result.get('host_port')}")
            else:
                logger.error("No container ID returned from start task")
        else:
            logger.error("Start task failed")
            
    except Exception as e:
        logger.error(f"Error in task demonstration: {str(e)}")

if __name__ == '__main__':
    demonstrate_create_task()