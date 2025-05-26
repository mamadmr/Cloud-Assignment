from pydantic import BaseModel

class TeamRequest(BaseModel):
    name: str

class TeamResponse(TeamRequest):
    id: int
    class Config:
        orm_mode = True
