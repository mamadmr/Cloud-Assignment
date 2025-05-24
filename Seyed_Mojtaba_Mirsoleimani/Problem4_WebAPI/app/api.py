from flask import Blueprint, request, jsonify
from .tasks import start_container_task, stop_container_task
from .models import db, TeamContainer

api_bp = Blueprint('api', __name__)

@api_bp.route("/assign", methods=["POST"])
def assign_container():
    data = request.get_json()
    task = start_container_task.delay(data["team_id"], data["challenge_id"])
    return jsonify({"status": "started", "task_id": task.id})

@api_bp.route("/remove", methods=["POST"])
def remove_container():
    data = request.get_json()
    task = stop_container_task.delay(data["team_id"], data["challenge_id"])
    return jsonify({"status": "removing", "task_id": task.id})
