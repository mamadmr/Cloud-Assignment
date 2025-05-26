from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class TeamChallenge(Base):
    __tablename__ = 'team_challenges'
    id           = Column(Integer, primary_key=True)
    team_id      = Column(String, nullable=False)
    challenge    = Column(String, nullable=False)
    container_id = Column(String, unique=True, nullable=True)
    address      = Column(String, nullable=True)
    status       = Column(String, default='pending')
    created_at   = Column(DateTime, default=datetime.utcnow)
