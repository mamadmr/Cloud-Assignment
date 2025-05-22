from pydantic import BaseModel

class AssignRequest(BaseModel):
    team_id: str
    challenge_id: str

class RemoveRequest(BaseModel):
    team_id: str
    challenge_id: str
    
class TeamCreateRequest(BaseModel):
    team_id: str
    team_name: str

class ChallengeCreateRequest(BaseModel):
    challenge_id: str
    name: str
    image: str
    port: int

