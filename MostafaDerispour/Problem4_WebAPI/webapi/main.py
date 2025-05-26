from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from my_celery_app.tasks import start_container, stop_container
from webapi.database import engine, SessionLocal
from webapi.models import Container, Team
from webapi import schemas
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assign")
async def assign_container(data: schemas.AssignRequest, db: Session = Depends(get_db)):
    # Call Celery to start the container
    result = start_container.delay(data.team_id, data.challenge_id)
    time.sleep(2)
    container_info = result.get(timeout=10)

    if container_info["status"] != "started":
        raise HTTPException(status_code=500, detail="Failed to start container")

    # Optional: Ensure team exists
    team = db.query(Team).filter_by(team_id=data.team_id).first()
    if not team:
        team = Team(team_id=data.team_id)
        db.add(team)
        db.commit()

    # Add container record
    container = Container(
        team_id=data.team_id,
        challenge_id=data.challenge_id,
        container_id=container_info["container_id"],
        port=3000
    )
    db.add(container)
    db.commit()

    return {"container_id": container.container_id, "port": 3000}

@app.post("/remove")
async def remove_container(data: schemas.AssignRequest, db: Session = Depends(get_db)):
    # Call Celery to stop the container
    result = stop_container.delay(data.team_id, data.challenge_id)
    time.sleep(2)
    stop_info = result.get(timeout=10)

    if stop_info["status"] != "stopped":
        raise HTTPException(status_code=500, detail="Failed to stop container")

    # Find and remove the container record
    container = db.query(Container).filter_by(team_id=data.team_id, challenge_id=data.challenge_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(container)
    db.commit()

    return {"status": "removed"}