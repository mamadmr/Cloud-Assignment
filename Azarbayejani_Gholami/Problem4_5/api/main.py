from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Base, TeamChallenge
from celery_app import celery
from celery.result import AsyncResult
import requests

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChallengeRequest(BaseModel):
    team_id: int   
    challenge_id: str

@app.post("/assign_challenge")
async def assign_challenge(data: ChallengeRequest, db: Session = Depends(get_db)):
    task = celery.send_task("start_ctf_container", args=[data.team_id, data.challenge_id])
    result = AsyncResult(task.id, app=celery).get(timeout=60)
    
    record = TeamChallenge(
        team_id=data.team_id,
        challenge_id=data.challenge_id,
        container_id=result["container_id"],
        container_url=result["url"]
    )
    db.add(record)
    db.commit()
    return result

@app.post("/remove_challenge")
async def remove_challenge(data: ChallengeRequest, db: Session = Depends(get_db)):
    record = db.query(TeamChallenge).filter_by(
        team_id=data.team_id,
        challenge_id=data.challenge_id
    ).first()
    if not record:
        return {"error": "Not found"}

    task = celery.send_task("stop_ctf_container", args=[record.container_id])
    AsyncResult(task.id, app=celery).get(timeout=60)
    db.delete(record)
    db.commit()
    return {"status": "removed"}


