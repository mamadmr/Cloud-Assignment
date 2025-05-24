from sqlalchemy import Column, Integer, String
from database import Base

class TeamChallenge(Base):
    __tablename__ = "team_challenges"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    challenge_id = Column(String, nullable=False)
    container_id = Column(String, nullable=False)
    container_url = Column(String, nullable=False)
