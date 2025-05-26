from pydantic import BaseModel

class AssignRequest(BaseModel):
    team_id: str
    challenge_id: str  