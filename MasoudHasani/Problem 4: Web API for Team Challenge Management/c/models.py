# models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///./ctf.db"
Base = declarative_base()

class ActiveContainer(Base):
    __tablename__ = "active_containers"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, index=True)
    challenge_id = Column(String, index=True)
    container_id = Column(String)
    container_address = Column(String)
