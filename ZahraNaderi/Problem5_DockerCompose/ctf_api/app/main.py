from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas, tasks
from fastapi import HTTPException

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/create-team/")
def create_team(req: schemas.TeamCreateRequest, db: Session = Depends(get_db)):
    existing_team = db.query(models.Team).filter_by(team_id=req.team_id).first()
    if existing_team:
        return {"error": "Team already exists"}
    try:
        new_team = models.Team(team_name=req.team_name, team_id=req.team_id) 
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return {"message": "Team created", "team_id": new_team.team_id, "team_name": new_team.team_name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/api/create-challenge/")
def create_challenge(req: schemas.ChallengeCreateRequest, db: Session = Depends(get_db)):
    existing_challenge = db.query(models.Challenge).filter_by(challenge_id=req.challenge_id).first()
    if existing_challenge:
        return {"error": "Challenge already exists"}
    try:
        new_challenge = models.Challenge(
            challenge_id=req.challenge_id,
            name=req.name,
            image=req.image,
            port=req.port
        )
        db.add(new_challenge)
        db.commit()
        db.refresh(new_challenge)
        return {"message": "Challenge created", "challenge_id": new_challenge.challenge_id, "name": new_challenge.name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/assign-container/")
def assign_container(req: schemas.AssignRequest, db: Session = Depends(get_db)):
    challenge = db.query(models.Challenge).filter_by(challenge_id=req.challenge_id).first()
    if not challenge:
        return {"error": "Challenge not found"}
    
    result = tasks.start_container.delay(challenge.image, {"80/tcp": None}, req.team_id, req.challenge_id)
    return {"task_id": result.id, "message": "Container starting..."}

@app.delete("/api/remove-container/")
def remove_container(req: schemas.RemoveRequest, db: Session = Depends(get_db)):
    container = db.query(models.Container).filter_by(team_id=req.team_id, challenge_id=req.challenge_id).first()
    if not container:
        return {"error": "No container assigned"}
    result = tasks.stop_container.delay(container.container_id)
    return {"task_id": result.id, "message": "Container stopping..."}

@app.get("/api/list-containers/")
def list_containers(db: Session = Depends(get_db)):
    containers = db.query(models.Container).all()
    return [{"team": c.team_id, "challenge": c.challenge_id, "url": c.address} for c in containers]

