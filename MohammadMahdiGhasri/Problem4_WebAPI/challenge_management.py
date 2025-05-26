from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from celery_docker_ctf import start_container, remove_container
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()

# Database setup for PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:I0UseStrongPasswordsLikeThis@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class TeamChallenge(Base):
    __tablename__ = "team_challenges"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, index=True)
    challenge_id = Column(String, index=True)
    container_name = Column(String, unique=True)
    container_id = Column(String)
    ip_address = Column(String)
    host_port = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic models
class TeamChallengeCreate(BaseModel):
    team_id: str
    challenge_id: str
    image_name: str

class TeamChallengeResponse(BaseModel):
    team_id: str
    challenge_id: str
    container_name: str
    container_id: str
    ip_address: str
    host_port: str
    status: str
    message: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assign-container/", response_model=TeamChallengeResponse)
async def assign_container(team_challenge: TeamChallengeCreate, db: Session = Depends(get_db)):
    """
    Assign a CTF container to a team based on team ID and challenge ID.
    """
    try:
        # Generate unique container name
        from celery_docker_ctf import generate_container_name
        container_name = generate_container_name()

        # Start container using Celery task
        start_result = start_container.delay(team_challenge.image_name, container_name)
        result = start_result.get()

        if result['status'] in ['created', 'started', 'already_running']:
            # Update database
            db_team_challenge = TeamChallenge(
                team_id=team_challenge.team_id,
                challenge_id=team_challenge.challenge_id,
                container_name=container_name,
                container_id=result['container_id'],
                ip_address=result['ip_address'],
                host_port=result['host_port']
            )
            db.add(db_team_challenge)
            db.commit()
            db.refresh(db_team_challenge)

            return TeamChallengeResponse(
                team_id=team_challenge.team_id,
                challenge_id=team_challenge.challenge_id,
                container_name=container_name,
                container_id=result['container_id'],
                ip_address=result['ip_address'],
                host_port=result['host_port'],
                status=result['status'],
                message=result['message']
            )
        else:
            raise HTTPException(status_code=400, detail=result['message'])

    except Exception as e:
        logger.error(f"Error assigning container: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to assign container: {str(e)}")

@app.delete("/remove-container/{team_id}/{challenge_id}", response_model=TeamChallengeResponse)
async def remove_container_endpoint(team_id: str, challenge_id: str, db: Session = Depends(get_db)):
    """
    Remove a CTF container assigned to a team using team ID and challenge ID.
    """
    try:
        # Find container in database
        db_team_challenge = db.query(TeamChallenge).filter(
            TeamChallenge.team_id == team_id,
            TeamChallenge.challenge_id == challenge_id
        ).first()

        if not db_team_challenge:
            raise HTTPException(status_code=404, detail="Container assignment not found")

        # Remove container using Celery task
        remove_result = remove_container.delay(db_team_challenge.container_name)
        result = remove_result.get()

        if result['status'] == 'removed':
            # Delete from database
            db.delete(db_team_challenge)
            db.commit()

            return TeamChallengeResponse(
                team_id=team_id,
                challenge_id=challenge_id,
                container_name=db_team_challenge.container_name,
                container_id=db_team_challenge.container_id,
                ip_address=db_team_challenge.ip_address,
                host_port=db_team_challenge.host_port,
                status=result['status'],
                message=result['message']
            )
        else:
            raise HTTPException(status_code=400, detail=result['message'])

    except Exception as e:
        logger.error(f"Error removing container: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to remove container: {str(e)}")

@app.get("/active-containers/", response_model=list[TeamChallengeResponse])
async def list_active_containers(db: Session = Depends(get_db)):
    """
    List all active container assignments.
    """
    try:
        containers = db.query(TeamChallenge).all()
        return [
            TeamChallengeResponse(
                team_id=c.team_id,
                challenge_id=c.challenge_id,
                container_name=c.container_name,
                container_id=c.container_id,
                ip_address=c.ip_address,
                host_port=c.host_port,
                status="active",
                message="Container is assigned"
            ) for c in containers
        ]
    except Exception as e:
        logger.error(f"Error listing active containers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list containers: {str(e)}")