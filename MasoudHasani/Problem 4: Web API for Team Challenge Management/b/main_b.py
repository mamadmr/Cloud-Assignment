from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import docker

# ---------------- Database setup ----------------
DATABASE_URL = "sqlite:///./ctf.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ActiveContainer(Base):
    __tablename__ = "active_containers"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, index=True)
    challenge_id = Column(String, index=True)
    container_id = Column(String)
    container_address = Column(String)

Base.metadata.create_all(bind=engine)

# ---------------- FastAPI setup ----------------
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Docker setup ----------------
docker_client = docker.from_env()

# ---------------- API endpoints ----------------

@app.post("/assign/")
def assign_container(team_id: str, challenge_id: str, db: Session = Depends(get_db)):
    image_name = f"ctf_challenge_{challenge_id}"

    try:
        container = docker_client.containers.run(
            image_name,
            detach=True,
            ports={"80/tcp": None}
        )
        container.reload()
        ip_address = container.attrs["NetworkSettings"]["IPAddress"]

        new_container = ActiveContainer(
            team_id=team_id,
            challenge_id=challenge_id,
            container_id=container.id,
            container_address=ip_address
        )
        db.add(new_container)
        db.commit()

        return {"container_address": ip_address}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/remove/")
def remove_container(team_id: str, challenge_id: str, db: Session = Depends(get_db)):
    container_record = db.query(ActiveContainer).filter_by(
        team_id=team_id, challenge_id=challenge_id
    ).first()

    if not container_record:
        return {"error": "No such container assigned"}

    try:
        container = docker_client.containers.get(container_record.container_id)
        container.stop()
        container.remove()
    except Exception as e:
        return {"warning": f"Could not stop/remove container from Docker: {str(e)}"}

    db.delete(container_record)
    db.commit()
    return {"message": "Container removed"}

@app.get("/active/")
def list_active_containers(db: Session = Depends(get_db)):
    containers = db.query(ActiveContainer).all()
    return [
        {
            "team_id": c.team_id,
            "challenge_id": c.challenge_id,
            "container_id": c.container_id,
            "container_address": c.container_address
        }
        for c in containers
    ]
