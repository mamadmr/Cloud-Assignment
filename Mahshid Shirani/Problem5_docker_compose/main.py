from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import SessionLocal, Container, Base, engine
from tasks import start_container, stop_container  # Import Celery tasks
import os
import time

app = FastAPI()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database schema at startup
Base.metadata.create_all(bind=engine)

class ChallengeRequest(BaseModel):
    team_id: str
    challenge_id: str

@app.post("/assign")
async def assign_container(req: ChallengeRequest, db: SessionLocal = Depends(get_db)):
    # Queue the start_container task
    task = start_container.delay(req.team_id, req.challenge_id)
    return {"message": "Container creation queued", "task_id": task.id}

@app.delete("/remove")
async def remove_container(req: ChallengeRequest, db: SessionLocal = Depends(get_db)):
    # Queue the stop_container task
    task = stop_container.delay(req.team_id, req.challenge_id)
    return {"message": "Container removal queued", "task_id": task.id}

@app.get("/containers")
def list_containers(db: SessionLocal = Depends(get_db)):
    return db.query(Container).all()

@app.get("/health")
def health_check():
    return {"status": "OK"}