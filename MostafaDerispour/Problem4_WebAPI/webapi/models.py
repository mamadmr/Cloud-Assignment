from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from webapi.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, unique=True, index=True, nullable=False)

    containers = relationship("Container", back_populates="team")

class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, ForeignKey("teams.team_id"), nullable=False)
    challenge_id = Column(String, nullable=False)
    container_id = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    team = relationship("Team", back_populates="containers")