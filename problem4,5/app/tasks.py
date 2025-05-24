from celery import Celery
import subprocess
import os
from app.models import Assignment, Challenge
from app.database import SessionLocal


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Celery configuration
app = Celery(
    'celery_tasks',
    broker=f'redis://{REDIS_HOST}:6379/0',
    backend=f'redis://{REDIS_HOST}:6379/1'
)

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ctf_db"

@app.task
def start_ctf_container(team_id, challenge_id):
    container_name = f"ctf_{team_id}_{challenge_id}"
    try:
        db = SessionLocal()
        try:
            challenge = db.query(Challenge).filter_by(id=challenge_id).first()
            if not challenge:
                return f"Challenge {challenge_id} not found."
            image_name = challenge.image_name
        finally:
            db.close()

        # Check if container already exists
        result = subprocess.run(
            ['docker', 'ps', '-a', '--filter', f'name=^{container_name}$', '--format', '{{.Names}}'],
            capture_output=True,
            text=True
        )
        if container_name in result.stdout.strip():
            subprocess.run(['docker', 'start', container_name], check=True)
        else:
            subprocess.run(['docker', 'run', '-d', '--name', container_name, image_name], check=True)

        # Get container's IP address
        ip_result = subprocess.run(
            ['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', container_name],
            capture_output=True,
            text=True
        )
        ip_address = ip_result.stdout.strip()
        container_url = f"http://{ip_address}:80"

        # Update database
        db = SessionLocal()
        try:
            assignment = db.query(Assignment).filter_by(team_id=team_id, challenge_id=challenge_id).first()
            if assignment:
                assignment.status = "running"
                assignment.url = container_url
            else:
                new_assignment = Assignment(
                    team_id=team_id,
                    challenge_id=challenge_id,
                    container_name=container_name,
                    status="running",
                    url=container_url
                )
                db.add(new_assignment)
            db.commit()
        finally:
            db.close()

        return f"Container '{container_name}' running at {container_url}"

    except subprocess.CalledProcessError as e:
        return f"Failed to start container: {e}"

@app.task
def stop_ctf_container(team_id, challenge_id):
    container_name = f"ctf_{team_id}_{challenge_id}"
    try:
        db = SessionLocal()
        try:
            assignment = db.query(Assignment).filter_by(team_id=team_id, challenge_id=challenge_id).first()
            if assignment:
                subprocess.run(['docker', 'stop', container_name], check=True)
                subprocess.run(['docker', 'rm', container_name], check=True)

                assignment.status = "removed"
                db.commit()

                return {
                    "message": f"Container '{container_name}' stopped and removed.",
                    "url": assignment.url
                }
            else:
                return {
                    "error": f"No assignment found for team {team_id} and challenge {challenge_id}."
                }
        finally:
            db.close()

    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to stop container: {e}"}