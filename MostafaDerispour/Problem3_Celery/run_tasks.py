from tasks import start_container, stop_container
import time
import subprocess

print(">>> Starting container...")
result = start_container.delay("alpine", "ctf_test")
start_info = result.get(timeout=15)
print("Start result:", start_info)


# Run 'docker ps' to list all running containers after 5 seconds
print(">>> Running 'sudo docker ps' after start")
try:
    result = subprocess.run(
        ["sudo", "docker", "ps"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    # Only print the result
    print(result.stdout.strip())  # Prints the list of running containers
except subprocess.CalledProcessError:
    print("❌ Failed to check container status.")

print(">>> Stopping container...")
stop_result = stop_container.delay("ctf_test")
stop_info = stop_result.get(timeout=15)
print("Stop result:", stop_info)

print(">>> Running 'sudo docker ps' after stoping")
try:
    result = subprocess.run(
        ["sudo", "docker", "ps"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    # Only print the result
    print(result.stdout.strip())  # Prints the list of running containers
except subprocess.CalledProcessError:
    print("❌ Failed to check container status.")
