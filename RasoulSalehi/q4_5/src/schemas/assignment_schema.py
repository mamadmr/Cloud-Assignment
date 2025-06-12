from pydantic import BaseModel

class AssignmentRequest(BaseModel):
    team_id: int
    task_id: int

class AssignmentResponse(BaseModel):
    team_id: int
    challenge_id: int
    container_name: str
    container_url: str
    status: str

    class Config:
        orm_mode = True
