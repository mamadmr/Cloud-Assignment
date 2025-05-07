from celery_app import app
import docker
import traceback

client = docker.from_env()

@app.task
def start_container(image_name, container_name=None):
    try:
        container = client.containers.run(
            image_name, 
            name=container_name,
            detach=True, 
            auto_remove=False,
            command="tail -f /dev/null"
        )
        return {'status': 'started', 'id': container.id, 'name': container.name}
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'traceback': traceback.format_exc()}

@app.task
def stop_container(container_id_or_name):
    try:
        container = client.containers.get(container_id_or_name)
        container.stop()
        return {'status': 'stopped', 'id': container.id, 'name': container.name}
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'traceback': traceback.format_exc()}
