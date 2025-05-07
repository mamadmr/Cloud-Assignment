# Import tasks to register them with the Celery app
from tasks import start_container, stop_container

# Stop a container
result = stop_container.delay(
    "c51b31ab3a20be12d615f8cee5d9a96f98bbd67679f898cd2511658c37917fca"
)
print(result.get())
