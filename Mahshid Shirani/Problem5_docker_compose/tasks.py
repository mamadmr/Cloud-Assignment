from celery_worker import celery_app
import docker
from database import SessionLocal, Container
import os
import time

# Robust Docker client with retries
def get_docker_client():
    max_retries = 3
    for i in range(max_retries):
        try:
            client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
            client.ping()
            return client
        except Exception as e:
            print(f"Docker connection failed (attempt {i+1}): {str(e)}")
            time.sleep(2)
    return None

@celery_app.task(bind=True)
def start_container(self, team_id: str, challenge_id: str):
    db = SessionLocal()
    try:
        client = get_docker_client()
        if not client:
            return {"error": "Docker connection failed"}
            
        container = client.containers.run(
            "nginx:latest",
            detach=True,
            name=f"ctf_{team_id}_{challenge_id}",
            ports={'80/tcp': None}
        )
        
        db_container = Container(
            team_id=team_id,
            challenge_id=challenge_id,
            container_id=container.id,
            status="active"
        )
        db.add(db_container)
        db.commit()
        return {"container_id": container.id}
    except Exception as e:
        self.retry(exc=e, countdown=60)
        return {"error": str(e)}
    finally:
        db.close()

@celery_app.task(bind=True)
def stop_container(self, team_id: str, challenge_id: str):
    db = SessionLocal()
    try:
        client = get_docker_client()
        if not client:
            return {"error": "Docker connection failed"}
            
        container = db.query(Container).filter_by(
            team_id=team_id,
            challenge_id=challenge_id
        ).first()
        
        if container:
            docker_container = client.containers.get(container.container_id)
            docker_container.stop()
            docker_container.remove()
            db.delete(container)
            db.commit()
            return {"message": "Container removed"}
        return {"error": "Container not found"}
    except Exception as e:
        self.retry(exc=e, countdown=60)
        return {"error": str(e)}
    finally:
        db.close()
