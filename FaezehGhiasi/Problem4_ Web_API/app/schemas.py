from pydantic import BaseModel

class ChallengeRequest(BaseModel):
    team_id: int
    challenge_id: int


class ChallengeResponse(BaseModel):
    team_id: int
    challenge_id: int
    container_name: str
    container_address: str
    status: str

    class Config:
        from_attributes = True
