# Import tasks to register them with the Celery app
from tasks import start_container, stop_container

# Start a container
result = start_container.delay("nginx:latest", "my_nginx_container")
print(result.get())  # Wait for the task to complete and get the result
