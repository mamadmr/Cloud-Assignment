from sqlalchemy import Column, Integer, String
from app.database import Base


class TeamChallenge(Base):
    __tablename__ = "team_challenges"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, index=True, nullable=False)
    challenge_id = Column(Integer, index=True, nullable=False)
    container_id = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    status = Column(String, nullable=False, default="running")
