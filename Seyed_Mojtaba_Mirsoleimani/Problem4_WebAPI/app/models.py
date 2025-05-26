from .database import db

class TeamContainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String, nullable=False)
    challenge_id = db.Column(db.String, nullable=False)
    container_id = db.Column(db.String, nullable=False)
    container_ip = db.Column(db.String, nullable=False)
