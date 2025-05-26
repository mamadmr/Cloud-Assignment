
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal, AssignedChallenge, init_db
from schemas import ChallengeRequest, ChallengeResponse
from tasks import start_container, stop_container

router = APIRouter(prefix="/api/v1", tags=["challenges"])


init_db()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CHALLENGE_IMAGES = {
    1: "pasapples/apjctf-todo-java-app:latest",
    2: "bkimminich/juice-shop",
}

CHALLENGE_IMAGES_PORTS = {
    1: 8080,
    2: 3000,
}


@router.post("/assign_challenge", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
def assign_challenge(
    request: ChallengeRequest,
    db: Session = Depends(get_db),
):
    image_name = CHALLENGE_IMAGES.get(request.challenge_id)
    if not image_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported challenge_id",
        )

    container_name = f"team{request.team_id}_challenge{request.challenge_id}"
    host_port = 3000 + request.team_id * 10 + request.challenge_id
    container_port = CHALLENGE_IMAGES_PORTS.get(request.challenge_id)
    

    dup = (
        db.query(AssignedChallenge)
        .filter_by(team_id=request.team_id, challenge_id=request.challenge_id)
        .first()
    )
    if dup:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Challenge already assigned to this team",
        )

    start_container.delay(image_name, container_name, host_port, container_port)

    container_address = f"http://localhost:{host_port}"

    assignment = AssignedChallenge(
        team_id=request.team_id,
        challenge_id=request.challenge_id,
        container_name=container_name,
        container_address=container_address,
        status="starting",
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment



@router.post("/remove_challenge",response_model=ChallengeResponse,status_code=status.HTTP_202_ACCEPTED,)
def remove_challenge(request: ChallengeRequest,db: Session = Depends(get_db),):
    container_name = f"team{request.team_id}_challenge{request.challenge_id}"

    assignment = (
        db.query(AssignedChallenge)
        .filter_by(team_id=request.team_id, challenge_id=request.challenge_id)
        .first()
    )
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found for this team",
        )
    
    if assignment.status == "stopping":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Challenge already stopped",)

    stop_container.delay(container_name)


    assignment.status = "stopping"
    db.commit()
    db.refresh(assignment)

    return assignment
