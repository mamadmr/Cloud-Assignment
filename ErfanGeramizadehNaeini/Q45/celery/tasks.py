from psycopg2.extras import RealDictCursor
import psycopg2
from celery import Celery
import os
import docker


app = Celery(
    'tasks',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://redis:6390/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6390/0'),
)

client = docker.from_env()


def get_pg_connection():
    return psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'localhost'),
        port=os.environ.get('POSTGRES_PORT', '5432'),
        dbname=os.environ.get('POSTGRES_DB', 'mydb'),
        user=os.environ.get('POSTGRES_USER', 'myuser'),
        password=os.environ.get('POSTGRES_PASSWORD', 'mypassword'),
        cursor_factory=RealDictCursor
    )


conn = get_pg_connection()


@app.task(name='tasks.add')  # just for test
def add(x, y):
    return x + y


@app.task(name='tasks.start')
def start_container(teamproblemid):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT p.image_name,tp.ip,tp.port as hostport, p.port as guestport  FROM cloud_teamproblem tp JOIN cloud_problem p ON tp.problem_id =p.number where tp.id=%s;""",
                    (teamproblemid,))

        row = cur.fetchone()
        image_name = row['image_name']
        hostport = row['hostport']
        guestport = row['guestport']
        print(
            f"Starting container with image {image_name} on port {hostport}:{guestport}")
        container = client.containers.run(
            image=image_name,
            name=None,
            ports={f"{guestport}/tcp": hostport},
            detach=True
        )

        cur.execute("""UPDATE cloud_teamproblem SET container_id=%s WHERE id=%s;""",
                    (container.id, teamproblemid))
        conn.commit()
        cur.close()
        return f"{container.id}"
    except docker.errors.APIError as e:
        return f"Error starting container: {str(e)}"


@app.task(name='tasks.stop')
def stop_container(teamproblemid):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT container_id FROM cloud_teamproblem WHERE id=%s;""",
                    (teamproblemid,))
        container_id = cur.fetchone()['container_id']
        container = client.containers.get(container_id=container_id)

        container.stop()

        cur.execute("""UPDATE cloud_teamproblem SET container_id=NULL WHERE id=%s;""",
                    (teamproblemid,))
        conn.commit()
        cur.close()
        container.remove(force=True)

        return f"Container {container_id} stopped"
    except docker.errors.NotFound:
        return f"Container {container_id} not found"
    except docker.errors.APIError as e:
        return f"Error stopping container: {str(e)}"
