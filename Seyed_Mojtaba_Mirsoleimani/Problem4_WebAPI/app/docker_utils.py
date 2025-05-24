import docker

client = docker.from_env()

def start_container(team_id, challenge_id):
    name = f"{team_id}_{challenge_id}"
    container = client.containers.run(
        "challenge_image", 
        detach=True,
        name=name,
        ports={"80/tcp": None}
    )
    ip = container.attrs["NetworkSettings"]["IPAddress"]
    return container.id, ip

def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
