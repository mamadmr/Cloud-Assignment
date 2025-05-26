from celery import Celery
import random
import string
import docker

app = Celery("tasks", broker=os.getenv("REDIS_BROKER"))
docker_client = docker.from_env()

used_ports = set()

@app.task
def create_container_task():
    try:
        port = random.randint(8000, 9000)
        while port in used_ports:
            port = random.randint(8000, 9000)
        used_ports.add(port)

        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        container = docker_client.containers.run(
            "alpine",
            name=name,
            command="sleep 3600",
            detach=True,
            ports={"80/tcp": port},
        )
        return {"name": name, "ip": "localhost", "port": port}
    except Exception as e:
        return {"error": str(e)}

@app.task
def delete_container_task(name):
    try:
        container = docker_client.containers.get(name)
        container.kill()
        container.remove()
        return {"status": "deleted"}
    except Exception as e:
        return {"error": str(e)}