from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, unique=True, index=True)
    team_name = Column(String)


class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(String, unique=True, index=True)
    name = Column(String)
    image = Column(String)
    port = Column(Integer)

class Container(Base):
    __tablename__ = "containers"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String)
    challenge_id = Column(String)
    container_id = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
