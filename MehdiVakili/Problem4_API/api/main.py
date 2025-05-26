from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, TeamChallenge
# from worker.tasks import start_ctf, stop_ctf
import os
from celery import Celery

celery_app = Celery(
    'api',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL').replace('/0', '/1'),
)

app = FastAPI()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class AssignReq(BaseModel):
    team_id: str
    challenge: str
    image: str

class RemoveReq(BaseModel):
    team_id: str
    challenge: str

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/assign")
async def assign(req: AssignReq):
    task = celery_app.send_task(
        'tasks.start_ctf',
        args=[req.image, req.team_id, req.challenge],
    )

    res = task.get(timeout=30)
    if not res:
        raise HTTPException(500, "Failed to start container")
    tc = TeamChallenge(
        team_id=req.team_id,
        challenge=req.challenge,
        container_id=res['container_id'],
        address=res['address'],
        status='running'
    )
    async with Session() as session:
        session.add(tc)
        await session.commit()
    return res

@app.post("/remove")
async def remove(req: RemoveReq):
    async with Session() as session:
        result = await session.execute(
            select(TeamChallenge)
            .where(TeamChallenge.team_id == req.team_id)
            .where(TeamChallenge.challenge == req.challenge)
        )
        tc = result.scalar_one_or_none()
        if not tc or not tc.container_id:
            raise HTTPException(404, "No active container")
        celery_app.send_task('tasks.stop_ctf', args=[tc.container_id])
        tc.status = 'stopped'
        await session.commit()
    return {"stopped": True}
