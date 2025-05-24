from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Container, Base, engine
from app.tasks import create_container_task, delete_container_task
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/create")
async def create_container(db: AsyncSession = Depends(get_db)):
    task = create_container_task.delay()
    while not task.ready():
        await asyncio.sleep(0.5)
    result = task.get()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    container = Container(name=result["name"], ip=result["ip"], port=result["port"])
    db.add(container)
    await db.commit()
    return result

@app.delete("/delete/{name}")
async def delete_container(name: str):
    task = delete_container_task.delay(name)
    while not task.ready():
        await asyncio.sleep(0.5)
    result = task.get()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
