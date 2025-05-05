import docker
from celery_app import app


client = docker.from_env() 
@app.task
def start_container(image_name):
    import docker
    client = docker.from_env()
    try:
        container = client.containers.run(
            image_name,
            command="sleep 60",  
            detach=True
        )
        return f"Started container: {container.name} (ID: {container.short_id})"
    except Exception as e:
        import traceback
        return f"Error: {str(e)}\n{traceback.format_exc()}"
    
    
@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Stopped container: {container_id}"
    except Exception as e:
        return f"Failed to stop: {str(e)}"

