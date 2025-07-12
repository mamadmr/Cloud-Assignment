from flask import Flask, request, jsonify
from celery import Celery
import psycopg2
import docker
import uuid
import socket
import random

# Flask app setup
app = Flask(__name__)

# Celery config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

docker_client = docker.from_env()

# PostgreSQL config
DB_CONFIG = {
    'dbname': 'ctfdb',
    'user': 'postgres',
    'password': '1111',
    'host': 'localhost'
}

def get_db_conn():
    return psycopg2.connect(**DB_CONFIG)

def find_free_port(start=3000, end=4000):
    while True:
        port = random.randint(start, end)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port

@app.route('/assign', methods=['POST'])
def assign_container():
    data = request.get_json()
    if not data or not all(k in data for k in ('team_id', 'challenge_id', 'image')):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    team_id = data['team_id']
    challenge_id = data['challenge_id']
    image = data['image']

    task = start_container_task.delay(team_id, challenge_id, image)
    result = task.get(timeout=60)
    return jsonify(result)

@app.route('/remove', methods=['POST'])
def remove_container():
    data = request.get_json()
    if not data or not all(k in data for k in ('team_id', 'challenge_id')):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    team_id = data['team_id']
    challenge_id = data['challenge_id']

    task = stop_container_task.delay(team_id, challenge_id)
    result = task.get(timeout=60)
    return jsonify(result)

@celery.task
def start_container_task(team_id, challenge_id, image):
    container_name = f"ctf_{team_id}_{challenge_id}"
    try:
        port = find_free_port()

        container = docker_client.containers.run(
            image,
            name=container_name,
            detach=True,
            ports={'3000/tcp': port} 
        )

        conn = get_db_conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO containers (id, team_id, challenge_id, container_id, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            str(uuid.uuid4()),
            team_id,
            challenge_id,
            container.id,
            f"http://localhost:{port}"
        ))

        conn.commit()
        cur.close()
        conn.close()

        return {'status': 'success', 'address': f"http://localhost:{port}"}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@celery.task
def stop_container_task(team_id, challenge_id):
    try:
        conn = get_db_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT container_id FROM containers WHERE team_id=%s AND challenge_id=%s
        """, (team_id, challenge_id))
        row = cur.fetchone()

        if not row:
            return {'status': 'error', 'message': 'Container not found'}

        container_id = row[0]

        try:
            container = docker_client.containers.get(container_id)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            pass  # Container already removed

        cur.execute("""
            DELETE FROM containers WHERE team_id=%s AND challenge_id=%s
        """, (team_id, challenge_id))
        conn.commit()

        cur.close()
        conn.close()

        return {'status': 'success', 'message': f"Container {container_id} stopped and removed."}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
