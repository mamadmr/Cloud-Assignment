from tasks import start_ctf_container, stop_ctf_container
import docker
import time

def manage_container(image_name="alpine", container_name="ctf-challenge"):
    client = docker.from_env()
    
    try:
        container = client.containers.get(container_name)
        print(f"Initial state: {container.status}")
    except:
        print("Initial state: No container")

    print("\nStarting container...")
    result = start_ctf_container.delay(image_name, container_name)
    while not result.ready():
        time.sleep(1)
    print(result.get())

    try:
        container = client.containers.get(container_name)
        print(f"State after start: {container.status}")
        container_id = container.id
    except:
        print("Failed to start container")
        return

    print("\nStopping container...")
    result = stop_ctf_container.delay(container_id)
    while not result.ready():
        time.sleep(1)
    print(result.get())

    try:
        container = client.containers.get(container_name)
        print(f"State after stop: {container.status}")
    except:
        print("State after stop: Removed")

if __name__ == "__main__":
    manage_container()
