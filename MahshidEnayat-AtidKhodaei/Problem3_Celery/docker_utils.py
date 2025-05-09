import docker

client = docker.from_env()

def start_ctf_container(image_name, container_name, port_map=None):
    try:
        container = client.containers.run(
            image=image_name,
            name=container_name,
            ports=port_map or {},
            detach=True
        )
        return {
            'status': 'success',
            'message': f"Container {container.name} started.",
            'container_id': container.id
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f"Error starting container: {str(e)}"
        }

def stop_ctf_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return {
            'status': 'success',
            'message': f"Container {container.name} with id {container_id} stopped and removed."
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f"Error stopping container: {str(e)}"
        }

