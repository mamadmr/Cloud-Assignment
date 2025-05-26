from celery import Celery
import subprocess

#Configure Celery to use Redis as its message broker.
app = Celery(
    'celery_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@app.task
def start_ctf_container(image_name, container_name):
    try:
        # check if container exists or not
        result = subprocess.run(
            ['docker', 'ps', '-a', '--filter', f'name=^{container_name}$', '--format', '{{.Names}}'],
            capture_output=True,
            text=True
        )
        if container_name in result.stdout.strip():
            # start if exists
            subprocess.run(['docker', 'start', container_name], check=True)
            return f"Existing container '{container_name}' started."
        else:
            # make if doesn't exist
            subprocess.run(['docker', 'run', '-d', '--name', container_name, image_name], check=True)
            return f"New container '{container_name}' started from image '{image_name}'."
    except subprocess.CalledProcessError as e:
        return f"Failed to start container: {e}"

@app.task
def stop_ctf_container(container_name):
    try:
        subprocess.run(['docker', 'stop', container_name], check=True)
        return f"Container '{container_name}' stopped."
    except subprocess.CalledProcessError as e:
        return f"Failed to stop container: {e}"
