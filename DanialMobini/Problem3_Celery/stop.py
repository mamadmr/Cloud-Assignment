# Import tasks to register them with the Celery app
from tasks import start_container, stop_container

# Stop a container
result = stop_container.delay(
    "7a77b8564ff9df9fea97a473ac9b1c3cd6a1ffe847ba113e50d0f3f748c4cd4a"
)
print(result.get())
