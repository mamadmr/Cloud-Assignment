# main_c.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from tasks import assign_container_task, remove_container_task
from models import Base, ActiveContainer, DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/assign_async/")
def assign_async(team_id: str, challenge_id: str):
    result = assign_container_task.delay(team_id, challenge_id)
    return {"task_id": result.id, "status": "assign task submitted"}

@app.delete("/remove_async/")
def remove_async(team_id: str, challenge_id: str, db: Session = Depends(get_db)):
    record = db.query(ActiveContainer).filter_by(team_id=team_id, challenge_id=challenge_id).first()
    if not record:
        return {"error": "No active container found for this team and challenge"}
    
    result = remove_container_task.delay(record.container_id)
    return {"task_id": result.id, "status": "remove task submitted"}

@app.get("/active/")
def get_active_containers(db: Session = Depends(get_db)):
    containers = db.query(ActiveContainer).all()
    return [
        {
            "team_id": c.team_id,
            "challenge_id": c.challenge_id,
            "container_id": c.container_id,
            "container_address": c.container_address
        }
        for c in containers
    ]

