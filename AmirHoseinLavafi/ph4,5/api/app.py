from flask import Flask, request, jsonify
import os, psycopg2
from tasks import start_container, stop_container

app = Flask(__name__)
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST")
)

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/assign', methods=['POST'])
def assign():
    data = request.get_json()
    result = start_container.delay(data["team_id"], data["challenge_id"])
    container_info = result.get(timeout=30)

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO team_challenges (team_id, challenge_id, container_id, container_address) VALUES (%s, %s, %s, %s)",
            (data["team_id"], data["challenge_id"], container_info["container_id"], container_info["address"])
        )
        conn.commit()
    return jsonify(container_info)

@app.route('/remove', methods=['POST'])
def remove():
    data = request.get_json()
    with conn.cursor() as cur:
        cur.execute("SELECT container_id FROM team_challenges WHERE team_id=%s AND challenge_id=%s", (data["team_id"], data["challenge_id"]))
        row = cur.fetchone()
        if row:
            stop_container.delay(row[0])
            cur.execute("DELETE FROM team_challenges WHERE team_id=%s AND challenge_id=%s", (data["team_id"], data["challenge_id"]))
            conn.commit()
            return jsonify({"status": "removed"})
        return jsonify({"error": "container not found"}), 404
