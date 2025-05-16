from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.tasks import start_container, stop_container
from app.database import SessionLocal
from app.models import Container

router = APIRouter()

# Pydantic model for JSON body
class ContainerRequest(BaseModel):
    team_id: str
    challenge_id: str

@router.post("/assign")
def assign_container(request: ContainerRequest):
    start_container.delay(request.team_id, request.challenge_id)
    return {"message": "Container creation started in background"}

@router.post("/remove")
def remove_container(request: ContainerRequest):
    stop_container.delay(request.team_id, request.challenge_id)
    return {"message": "Container removal started in background"}

@router.get("/container_address")
def get_container_address(
    team_id: str = Query(...),
    challenge_id: str = Query(...)
):
    db = SessionLocal()
    container = db.query(Container).filter_by(
        team_id=team_id,
        challenge_id=challenge_id
    ).first()
    db.close()

    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    
    return {"container_address": container.container_address}

