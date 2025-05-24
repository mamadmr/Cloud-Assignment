import os
from celery import Celery
from app.models import db, TeamContainer
from flask import Flask
from .docker_utils import start_container, stop_container

celery = Celery("tasks", broker=os.getenv("REDIS_BROKER_URL"))

@celery.task()
def start_container_task(team_id, challenge_id):
    container_id, ip = start_container(team_id, challenge_id)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    db.init_app(app)
    with app.app_context():
        team_container = TeamContainer(
            team_id=team_id,
            challenge_id=challenge_id,
            container_id=container_id,
            container_ip=ip
        )
        db.session.add(team_container)
        db.session.commit()

@celery.task()
def stop_container_task(team_id, challenge_id):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    db.init_app(app)
    with app.app_context():
        record = TeamContainer.query.filter_by(team_id=team_id, challenge_id=challenge_id).first()
        if record:
            stop_container(record.container_id)
            db.session.delete(record)
            db.session.commit()
