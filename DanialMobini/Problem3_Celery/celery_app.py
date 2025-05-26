from celery import Celery

# Configure Celery to use Redis as the message broker
app = Celery(
    "container_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Import tasks to register them with the Celery app
import tasks
