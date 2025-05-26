from docker_tasks import start_container, stop_container
from time import sleep
import docker

client = docker.from_env()

def print_container_status():
    containers = client.containers.list(all=True)
    if containers:
        for container in containers:
            print(f"Container {container.name} - Status: {container.status} - ID: {container.id}")
    else:
        print("No containers running.")

print("before running tasks:")
print_container_status()

# running start task
result = start_container.apply_async(args=["ctf_challenge", "ctf_image", {"5000/tcp": 5000}])
sleep(5)

print("\nafter running start task:")
print_container_status()

container_id = result.result["container_id"]
print(f"\ncontainer ID: {container_id}")

# running stop tasl
stop_result = stop_container.apply_async(args=[container_id])

try:
    result_data = stop_result.get(timeout=20)
    print(f"\n stop resualt: {result_data}")
except Exception as e:
    print(f"\n⛔ error on stop_result.get(): {e}")

print("\nafter running stop tast:")
print_container_status()
