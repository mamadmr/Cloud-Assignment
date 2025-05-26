from fastapi import FastAPI
from app import tasks, database, models
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel

class AssignmentRequest(BaseModel):
    team_id: int
    challenge_id: int

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assign")
def assign_container(request: AssignmentRequest, db: Session = Depends(get_db)):
    task = tasks.start_ctf_container.delay(request.team_id, request.challenge_id)
    return {"status": "assigned", "task_id": task.id}

@app.post("/remove")
def remove_container(request: AssignmentRequest, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter_by(team_id=request.team_id, challenge_id=request.challenge_id).first()
    if assignment:
        tasks.stop_ctf_container.delay(request.team_id, request.challenge_id)
        return {
            "status": "removing",
            "container_name": assignment.container_name,
            "url": assignment.url
        }
    return {"error": "not found"}