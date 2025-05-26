from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image_name = Column(String)

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    container_name = Column(String)
    url = Column(String)
    status = Column(String, default="stopped")