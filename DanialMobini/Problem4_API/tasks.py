from celery import Celery
import docker

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)
client = docker.from_env()


@app.task
def start_container(team_id, challenge_id, image_name):
    try:
        # Start container with auto port mapping
        container = client.containers.run(
            image_name,
            detach=True,
            publish_all_ports=True,  # Let Docker assign all exposed ports
        )

        # Wait for container to be running and get updated attributes
        container.reload()

        # Get the port mappings
        ports = container.attrs["NetworkSettings"]["Ports"]

        if not ports:
            raise ValueError("Container has no exposed ports")

        # Find the first exposed port and its mapping
        for container_port, host_ports in ports.items():
            if host_ports:  # If there are host port mappings
                host_port = host_ports[0]["HostPort"]
                protocol = container_port.split("/")[-1]  # Get tcp/udp
                return {
                    "container_id": container.id,
                    "address": f"http://localhost:{host_port}",
                    "protocol": protocol,
                }

        raise ValueError("No port mappings found")

    except Exception as e:
        # Clean up if something went wrong
        if "container" in locals():
            try:
                container.stop()
                container.remove()
            except:
                pass
        raise e


@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return True
    except docker.errors.NotFound:
        return False  # Container already removed
    except Exception as e:
        raise e
