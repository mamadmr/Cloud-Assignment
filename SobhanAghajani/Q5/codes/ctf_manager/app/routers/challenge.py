from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.tasks import start_container, stop_container

router = APIRouter()

# Pydantic model for JSON body
class ContainerRequest(BaseModel):
    team_id: str
    challenge_id: str

@router.post("/assign")
def assign_container(request: ContainerRequest):
    result = start_container.delay(request.team_id, request.challenge_id)
    
    try:
        # Wait for the result (container address) for up to 30 seconds
        container_address = result.get(timeout=30)
        return {"container_address": container_address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign container: {str(e)}")

@router.post("/remove")
def remove_container(request: ContainerRequest):
    result = stop_container.delay(request.team_id, request.challenge_id)

    try:
        removed_info = result.get(timeout=30)
        return {"removed_container": removed_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove container: {str(e)}")

