from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import SessionLocal, initialize_database
from schemas.assignment_schema import AssignmentRequest, AssignmentResponse
from workers.docker_tasks import launch_container, terminate_container
from entities.assignment import Assignment  
from fastapi import Query
from typing import List, Optional
from entities.task import Task
from entities.team import Team
from schemas.task_schema import TaskRequest, TaskResponse
from schemas.team_schema import TeamRequest, TeamResponse


router = APIRouter(prefix="/api/v1", tags=["assignments"])

initialize_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/assign", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_challenge(request: AssignmentRequest, db: Session = Depends(get_db)):
    team = db.query(Team).filter_by(id=request.team_id).first()
    if not team:
        raise HTTPException(status_code=400, detail="Invalid team ID")

    task = db.query(Task).filter_by(id=request.task_id).first()
    if not task:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    existing = db.query(Assignment).filter_by(team_id=request.team_id, challenge_id=request.task_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Task already assigned to team")

    container_name = f"team{request.team_id}_task{request.task_id}"
    host_port = 3000 + request.team_id * 10 + request.task_id

    launch_container.delay(task.docker_image, container_name, host_port, task.container_port)

    assignment = Assignment(
        team_id=request.team_id,
        challenge_id=request.task_id,  
        container_name=container_name,
        container_url=f"http://localhost:{host_port}",
        status="starting",
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


@router.post("/remove", response_model=AssignmentResponse, status_code=status.HTTP_202_ACCEPTED)
def remove_challenge(request: AssignmentRequest, db: Session = Depends(get_db)):
    # ✅ Check if assignment exists
    assignment = db.query(Assignment).filter_by(team_id=request.team_id, challenge_id=request.task_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found for this team and task")

    if assignment.status == "stopping":
        raise HTTPException(status_code=409, detail="Task already stopping for this team")

    terminate_container.delay(assignment.container_name)

    db.delete(assignment)
    db.commit()

    return assignment



@router.get("/assignments", response_model=List[AssignmentResponse])
def list_assignments(team_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    List all assignments or filter by team_id.
    """
    if team_id is not None:
        assignments = db.query(Assignment).filter_by(team_id=team_id).all()
    else:
        assignments = db.query(Assignment).all()
    return assignments


@router.get("/assignment", response_model=AssignmentResponse)
def get_assignment(team_id: int = Query(...), challenge_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Get a specific assignment by team_id and challenge_id.
    """
    assignment = db.query(Assignment).filter_by(team_id=team_id, challenge_id=challenge_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment



@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskRequest, db: Session = Depends(get_db)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.post("/teams", response_model=TeamResponse)
def create_team(team: TeamRequest, db: Session = Depends(get_db)):
    new_team = Team(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@router.get("/teams", response_model=List[TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()
