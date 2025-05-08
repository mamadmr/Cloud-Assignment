from celery import Celery

app = Celery(
    'client',
    broker='redis://localhost:6391/0',
    backend='redis://localhost:6391/0'
)
# initial test
print("Sending test task...")
result = app.send_task('tasks.add', args=[3, 4])
print("Result:", result.get(timeout=10))

print("Starting container...")
container_id = app.send_task('tasks.start', args=[
    'pasapples/apjctf-todo-java-app:latest'])
id = container_id.get(timeout=1000)
print("Container ID:", id)  # pulling may take time

result = app.send_task('tasks.stop', args=[id])
print("Sent stop task, waiting for result...")
print(result.get(timeout=20))
