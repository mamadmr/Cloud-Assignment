from celery import Celery
import docker
import psycopg2
import time

app = Celery('tasks', broker='redis://redis:6379/0')

def get_docker_client():
    return docker.from_env()

def get_db_conn():
    return psycopg2.connect(
        host="db",
        database="ctfdb",
        user="postgres",
        password="1111"
    )

@app.task
def start_container_task(team_id, challenge):
    client = get_docker_client()
    image = {
        "juice": "bkimminich/juice-shop",
        "todo": "pasapples/apjctf-todo-java-app:latest"
    }[challenge]

    container_name = f"{challenge}_{team_id}"

    container = client.containers.run(
        image,
        name=container_name,
        detach=True,
        ports={'3000/tcp': None},
        labels={"team_id": str(team_id), "challenge": challenge}
    )

    port = None
    for _ in range(10):
        container.reload()
        port_bindings = container.attrs['NetworkSettings']['Ports'].get('3000/tcp')
        if port_bindings and len(port_bindings) > 0:
            port = port_bindings[0]['HostPort']
            break
        time.sleep(0.5)

    if port is None:
        container.stop()
        container.remove()
        raise Exception("Port 3000 is not mapped by Docker after waiting.")

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO container_info (team_id, challenge, container_name, host_port) VALUES (%s, %s, %s, %s)",
                (team_id, challenge, container_name, port))
    conn.commit()
    cur.close()
    conn.close()

    return f"Started container {container.name} on port {port}"

@app.task
def stop_container_task(team_id, challenge):
    client = get_docker_client()
    container_name = f"{challenge}_{team_id}"
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()

        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM container_info WHERE team_id=%s AND challenge=%s",
                    (team_id, challenge))
        conn.commit()
        cur.close()
        conn.close()

        return f"Stopped and removed container {container_name}"
    except Exception as e:
        return str(e)
