from tasks import start_container, stop_container
import time

print("Waiting for container to start…")
result = start_container.delay("nginx:alpine", ports={"8080/tcp": 8080})
container_id = result.get(timeout=20)
print("Started container:", container_id)

time.sleep(5)

print("Stopping container…")
stop_result = stop_container.delay(container_id)
print(stop_result.get(timeout=20))
