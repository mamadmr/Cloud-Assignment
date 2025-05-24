from fastapi import FastAPI, HTTPException, Depends
from database import Base, engine, SessionLocal, Container

from sqlalchemy.orm import Session
from pydantic import BaseModel
import docker

from database import SessionLocal, Base, Container

app = FastAPI()
client = docker.from_env()

Base.metadata.create_all(bind=engine)


# In-memory registry to track running container objects by (team_id, challenge_id)
container_registry = {}

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChallengeRequest(BaseModel):
    team_id: str
    challenge_id: str

def get_container_name(team_id, challenge_id):
    return f"nginx_{team_id}_{challenge_id}"

@app.post("/assign")
def assign_container(req: ChallengeRequest):
    key = (req.team_id, req.challenge_id)

    # Check if container already tracked in memory
    if key in container_registry:
        container = container_registry[key]
        container.reload()
        host_port = container.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
        return {"message": "Already assigned", "address": f"http://localhost:{host_port}"}

    try:
        container = client.containers.run(
            image="nginx:latest",
            detach=True,
            name=get_container_name(req.team_id, req.challenge_id),
            ports={'80/tcp': None},  # nginx listens on port 80
            network_mode="bridge"
        )
        container.reload()
        host_port = container.attrs['NetworkSettings']['Ports']['80/tcp'][0]['HostPort']
        container_registry[key] = container

        # Save container info to DB
        db = SessionLocal()
        existing = db.query(Container).filter_by(team_id=req.team_id, challenge_id=req.challenge_id).first()
        if existing:
            existing.container_id = container.id
            existing.host_port = host_port
            existing.status = "active"
        else:
            new_container = Container(
                team_id=req.team_id,
                challenge_id=req.challenge_id,
                container_id=container.id,
                host_port=host_port,
                status="active"
            )
            db.add(new_container)
        db.commit()
        db.close()

        return {
            "message": "Container assigned",
            "address": f"http://localhost:{host_port}"
        }

    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/remove")
def remove_container(req: ChallengeRequest, db: Session = Depends(get_db)):
    container = db.query(Container).filter_by(
        team_id=req.team_id,
        challenge_id=req.challenge_id
    ).first()

    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    address = f"http://localhost:{container.host_port}"

    db.delete(container)
    db.commit()

    return {"message": "Container removed", "address": address}



@app.get("/containers")
def list_all_containers():
    db = SessionLocal()
    containers = db.query(Container).all()
    db.close()
    return [c.__dict__ for c in containers]


@app.get("/active")
def list_active_containers(db: Session = Depends(get_db)):
    containers = db.query(Container).filter(Container.status == "active").all()
    return [
        {
            "team_id": c.team_id,
            "challenge_id": c.challenge_id,
            "host_port": c.host_port
        } for c in containers
    ]
