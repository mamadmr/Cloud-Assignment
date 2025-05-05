from tasks import start_container, stop_container
from time import sleep 

# Start a container
# using nginx image for testing that exits on my own local repository
result_start = start_container.delay('hello-world:latest', 'ctf-hello-world')
print(result_start.get(timeout=60))

time_to_sleep = 5
print(f"wait for {time_to_sleep} seconds")
sleep(time_to_sleep)

# Stop the container
result_stop = stop_container.delay('ctf-hello-world')
print(result_stop.get(timeout=60))

