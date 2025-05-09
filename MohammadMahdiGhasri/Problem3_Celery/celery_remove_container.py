from celery_docker_ctf import remove_container
import docker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Docker client
docker_client = docker.from_env()

def demonstrate_remove_task():
    """
    Prompt for container name and initiate removal task if it exists.
    """
    container_name = input("Enter container name to remove (e.g., ctf_challenge_001): ").strip()
    
    # Check if container exists
    existing_containers = docker_client.containers.list(
        all=True,
        filters={'name': container_name}
    )
    
    if not existing_containers:
        logger.info(f"Container {container_name} does not exist")
        print(f"Container {container_name} does not exist")
        return
    
    try:
        logger.info(f"Initiating container remove task for {container_name}...")
        remove_result = remove_container.delay(container_name)
        remove_result.wait()
        
        if remove_result.successful():
            result = remove_result.get()
            logger.info(f"Remove task result: {result}")
            print(f"Remove task result: {result}")
        else:
            logger.error("Remove task failed")
            print("Remove task failed")
            
    except Exception as e:
        logger.error(f"Error in remove task demonstration: {str(e)}")
        print(f"Error in remove task demonstration: {str(e)}")

if __name__ == '__main__':
    demonstrate_remove_task()