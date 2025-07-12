# import docker
# from celery_app import app

# client = docker.from_env()

# @app.task
# def start_container(image_name):
#     try:
#         container = client.containers.run(image_name, detach=True)
#         return container.id
#     except Exception as e:
#         return f"Error: {str(e)}"


# @app.task
# def stop_container(container_id):
#     try:
#         container = client.containers.get(container_id)
#         container.stop()
#         return f"Stopped container {container_id}"
#     except Exception as e:
#         return f"Error: {str(e)}"

######################################################################
from celery import Celery
import docker
import os

app = Celery('tasks', broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))
client = docker.from_env()

@app.task
def start_container(team_id, challenge_id):
    if challenge_id == 1:
        image = "bkimminich/juice-shop"
        expose_port = '3000'
    else:
        image = "pasapples/apjctf-todo-java-app:latest"
        expose_port = '8080'

    container = client.containers.run(
        image,
        detach=True,
        ports={f'{expose_port}/tcp': None} 
    )
    container.reload()
    host_port = container.attrs['NetworkSettings']['Ports'][f'{expose_port}/tcp'][0]['HostPort']
    return {"container_id": container.id, "address": f"localhost:{host_port}"}

@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return {"status": "stopped"}
    except Exception as e:
        return {"error": str(e)}
