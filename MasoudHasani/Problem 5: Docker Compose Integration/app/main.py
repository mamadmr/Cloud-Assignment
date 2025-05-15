from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, ContainerInfo
from tasks import assign_container_task, remove_container_task

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assign/")
def assign_container(team_id: str, challenge_id: str, db: Session = Depends(get_db)):
    result = assign_container_task.delay(team_id, challenge_id)
    import time
    time.sleep(2)  # Let task start and potentially finish fast
    async_result = result.get(timeout=10)
    if async_result['status'] == 'success':
        return async_result
    else:
        raise HTTPException(status_code=400, detail=async_result['message'])

@app.get("/containers/")
def list_containers(db: Session = Depends(get_db)):
    containers = db.query(ContainerInfo).all()
    return [
        {
            "team_id": c.team_id,
            "challenge_id": c.challenge_id,
            "container_id": c.container_id
        }
        for c in containers
    ]

@app.delete("/remove/")
def remove_container(team_id: str, challenge_id: str, db: Session = Depends(get_db)):
    result = remove_container_task.delay(team_id, challenge_id)
    import time
    time.sleep(2)
    async_result = result.get(timeout=10)
    if async_result['status'] == 'success':
        return async_result
    else:
        raise HTTPException(status_code=400, detail=async_result['message'])
