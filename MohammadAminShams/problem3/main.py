from tasks import start_container, stop_container
from time import sleep
import os

# Start a container
print("\n\nStarting container...\n")
result_start = start_container.delay('hello-world:latest', 'ctf-hello-world')
print(result_start.get(timeout=60))


# Wait for a moment to observe the running container
time_to_sleep = 5

# before creating hello-world 
os.system("docker ps")  # Executes the command

print(f"\nwait for {time_to_sleep} seconds\n")
sleep(time_to_sleep)

# Stop the container
print("\n\nStopping container...\n")
# after stop hello-world 
os.system("docker ps")  # Executes the command


result_stop = stop_container.delay('ctf-hello-world')
print(result_stop.get(timeout=60))