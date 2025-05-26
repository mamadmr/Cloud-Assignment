from tasks import start_container, stop_container
from time import sleep
import os

print("\n\nStarting container...\n")
result_start = start_container.delay('hello-world:latest', 'ctf-hello-world')
print(result_start.get(timeout=60))


time_to_sleep = 5

os.system("docker ps")

print(f"\nwait for {time_to_sleep} seconds\n")
sleep(time_to_sleep)

print("\n\nStopping container...\n")
os.system("docker ps") 


result_stop = stop_container.delay('ctf-hello-world')
print(result_stop.get(timeout=60))
