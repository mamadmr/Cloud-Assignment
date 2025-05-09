import docker
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery with Redis as the message broker
app = Celery(
    'celery_docker_ctf',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_time_limit=360,
    task_acks_late=True,
    worker_prefetch_multiplier=1
)

# Initialize Docker client
docker_client = docker.from_env()

def generate_container_name():
    """
    Generate a unique container name with incremental ID.
    
    Returns:
        str: Unique container name (e.g., 'ctf_challenge_001')
    """
    index = 1
    base_challenge_id = "challenge"
    while True:
        container_name = f"ctf_{base_challenge_id}_{index:03d}"
        existing = docker_client.containers.list(all=True, filters={'name': container_name})
        if not existing:
            return container_name
        index += 1

def get_available_port():
    """
    Find an available host port in the range 8000-9000.
    
    Returns:
        int: Available port number
    """
    used_ports = set()
    for container in docker_client.containers.list(all=True):
        if container.attrs['NetworkSettings']['Ports']:
            for port in container.attrs['NetworkSettings']['Ports'].values():
                if port and port[0]['HostPort']:
                    used_ports.add(int(port[0]['HostPort']))
    
    for port in range(8000, 9001):
        if port not in used_ports:
            return port
    raise Exception("No available ports in range 8000-9000")

@app.task(bind=True)
def start_container(self, image_name, container_name):
    """
    Celery task to start a Docker container with unique IP and port.
    
    Args:
        image_name (str): Docker image name for the challenge
        container_name (str): Unique name for the container
    
    Returns:
        dict: Container information including ID, IP, port, and status
    """
    try:
        # Check if container already exists
        existing_containers = docker_client.containers.list(
            all=True,
            filters={'name': container_name}
        )
        
        if existing_containers:
            container = existing_containers[0]
            if container.status == 'running':
                network_settings = container.attrs['NetworkSettings']
                ip_address = network_settings['Networks']['ctf_network']['IPAddress']
                ports = network_settings['Ports']['80/tcp']
                host_port = ports[0]['HostPort'] if ports else None
                return {
                    'status': 'already_running',
                    'container_id': container.id,
                    'ip_address': ip_address,
                    'host_port': host_port,
                    'message': f'Container {container_name} is already running'
                }
            
            # Start existing container if not running
            container.start()
            network_settings = container.attrs['NetworkSettings']
            ip_address = network_settings['Networks']['ctf_network']['IPAddress']
            ports = network_settings['Ports']['80/tcp']
            host_port = ports[0]['HostPort'] if ports else None
            return {
                'status': 'started',
                'container_id': container.id,
                'ip_address': ip_address,
                'host_port': host_port,
                'message': f'Existing container {container_name} started'
            }

        # Ensure ctf_network exists
        try:
            docker_client.networks.get('ctf_network')
        except docker.errors.NotFound:
            docker_client.networks.create(
                name='ctf_network',
                driver='bridge',
                ipam=docker.types.IPAMConfig(
                    pool_configs=[
                        docker.types.IPAMPool(
                            subnet='172.20.0.0/16',
                            gateway='172.20.0.1'
                        )
                    ]
                )
            )

        # Generate unique IP address
        used_ips = set()
        for container in docker_client.containers.list(all=True):
            if container.attrs['NetworkSettings']['Networks'].get('ctf_network'):
                used_ips.add(container.attrs['NetworkSettings']['Networks']['ctf_network']['IPAddress'])
        
        ip_address = None
        for i in range(2, 255):
            candidate_ip = f"172.20.0.{i}"
            if candidate_ip not in used_ips:
                ip_address = candidate_ip
                break
        if not ip_address:
            raise Exception("No available IP addresses in subnet")

        # Get available host port
        host_port = get_available_port()

        # Create and start new container
        container = docker_client.containers.run(
            image_name,
            name=container_name,
            detach=True,
            ports={'80/tcp': host_port},
            mem_limit='512m',
            cpu_period=100000,
            cpu_quota=50000,
            network='ctf_network',
            extra_hosts={'host.docker.internal': 'host-gateway'},
            dns=['8.8.8.8'],
            dns_search=['.'],
            hostname=container_name,
            domainname='ctf.local'
        )
        
        # Connect container to network with specific IP
        network = docker_client.networks.get('ctf_network')
        network.disconnect(container)
        network.connect(container, ipv4_address=ip_address)
        
        logger.info(f"Started container {container.id} for {container_name} with IP {ip_address} and port {host_port}")
        return {
            'status': 'created',
            'container_id': container.id,
            'ip_address': ip_address,
            'host_port': host_port,
            'message': f'New container {container_name} created and started'
        }

    except SoftTimeLimitExceeded:
        logger.error(f"Timeout starting container {container_name}")
        raise
    except docker.errors.ImageNotFound:
        logger.error(f"Image {image_name} not found for {container_name}")
        return {
            'status': 'error',
            'message': f'Image {image_name} not found'
        }
    except Exception as e:
        logger.error(f"Error starting container {container_name}: {str(e)}")
        return {
            'status': 'error',
            'message': f'Failed to start container: {str(e)}'
        }

@app.task(bind=True)
def remove_container(self, container_name):
    """
    Celery task to remove a Docker container by name.
    
    Args:
        container_name (str): Name of the container to remove
    
    Returns:
        dict: Status of the remove operation
    """
    try:
        # Check if container exists
        existing_containers = docker_client.containers.list(
            all=True,
            filters={'name': container_name}
        )
        
        if not existing_containers:
            logger.info(f"Container {container_name} does not exist")
            return {
                'status': 'not_found',
                'message': f'Container {container_name} does not exist'
            }
        
        container = existing_containers[0]
        container_id = container.id
        
        # Stop container if running
        if container.status == 'running':
            container.stop()
            logger.info(f"Stopped container {container_id} ({container_name})")
        
        # Remove container
        container.remove()
        logger.info(f"Removed container {container_id} ({container_name})")
        
        return {
            'status': 'removed',
            'container_id': container_id,
            'message': f'Container {container_name} removed successfully'
        }
    
    except SoftTimeLimitExceeded:
        logger.error(f"Timeout removing container {container_name}")
        raise
    except docker.errors.NotFound:
        logger.error(f"Container {container_name} not found")
        return {
            'status': 'error',
            'message': f'Container {container_name} not found'
        }
    except Exception as e:
        logger.error(f"Error removing container {container_name}: {str(e)}")
        return {
            'status': 'error',
            'message': f'Failed to remove container: {str(e)}'
        }