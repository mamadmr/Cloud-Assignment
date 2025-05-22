# File: src/entities/assignment.py
from sqlalchemy import Column, Integer, String
from config.db import Base

class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = {'extend_existing': True}  

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, index=True)
    challenge_id = Column(Integer, index=True)
    container_name = Column(String, index=True)
    container_url = Column(String)
    status = Column(String)