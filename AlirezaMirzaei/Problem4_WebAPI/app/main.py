from fastapi import FastAPI, HTTPException
from app.schemas import AssignRequest, AssignResponse, RemoveRequest, RemoveResponse
from app.database import engine, Base, SessionLocal
from app.models import TeamChallenge
from app.tasks import start_challenge, stop_challenge
import uvicorn

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CTF Challenge Manager")


@app.post("/assign", response_model=AssignResponse)
def assign_challenge(req: AssignRequest):
    result = start_challenge.delay(req.team_id, req.challenge_id)
    res = result.get(timeout=30)
    return res


@app.post("/remove", response_model=RemoveResponse)
def remove_challenge(req: RemoveRequest):
    result = stop_challenge.delay(req.team_id, req.challenge_id)
    res = result.get(timeout=30)
    return res


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
