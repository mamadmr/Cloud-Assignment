# app.py
from flask import Flask, request, jsonify
from models import SessionLocal, Container, init_db
from docker_tasks import start_container, stop_container

app = Flask(__name__)
init_db()

@app.route("/assign", methods=["POST"])
def assign_container():
    data = request.json
    team_id = data["team_id"]
    challenge_id = data["challenge_id"]
    image_name = data["image_name"]
    res = start_container.delay(team_id, challenge_id, image_name)
    return jsonify({"message": "Starting container...", "task_id": res.id}), 202

@app.route("/remove", methods=["POST"])
def remove_container():
    data = request.json
    team_id = data["team_id"]
    challenge_id = data["challenge_id"]
    res = stop_container.delay(team_id, challenge_id)
    return jsonify({"message": "Stopping container...", "task_id": res.id}), 202

@app.route("/status/<team_id>/<challenge_id>", methods=["GET"])
def get_status(team_id, challenge_id):
    db = SessionLocal()
    container = db.query(Container).filter_by(team_id=team_id, challenge_id=challenge_id).first()
    db.close()
    if container:
        return jsonify({
            "container_id": container.container_id,
            "address": container.address
        })
    return jsonify({"message": "Not found"}), 404

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)

