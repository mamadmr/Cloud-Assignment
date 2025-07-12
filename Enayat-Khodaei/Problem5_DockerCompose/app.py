from flask import Flask, request, jsonify
from tasks import start_container_task, stop_container_task
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@db:5432/ctfdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ContainerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String(50), nullable=False)
    challenge = db.Column(db.String(50), nullable=False)
    container_name = db.Column(db.String(100), nullable=False)
    host_port = db.Column(db.String(10), nullable=False)

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    team_id = data['team_id']
    challenge = data['challenge']

    task = start_container_task.delay(team_id, challenge)
    return jsonify({"status": "starting", "task_id": task.id})

@app.route('/stop', methods=['POST'])
def stop():
    data = request.get_json()
    team_id = data['team_id']
    challenge = data['challenge']

    task = stop_container_task.delay(team_id, challenge)
    return jsonify({"status": "stopping", "task_id": task.id})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
