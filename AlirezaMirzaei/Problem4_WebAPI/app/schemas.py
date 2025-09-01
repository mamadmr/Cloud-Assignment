# app/schemas.py
from pydantic import BaseModel


class AssignRequest(BaseModel):
    team_id: int
    challenge_id: int


class AssignResponse(BaseModel):
    team_id: int
    challenge_id: int
    container_id: str
    address: str
    status: str


class RemoveRequest(BaseModel):
    team_id: int
    challenge_id: int


class RemoveResponse(BaseModel):
    team_id: int
    challenge_id: int
    container_id: str
    status: str
