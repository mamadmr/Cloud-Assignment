from sqlalchemy import Column, String
from db import Base

class ContainerInfo(Base):
    __tablename__ = "containers"

    team_id = Column(String, primary_key=True, index=True)
    challenge_id = Column(String, primary_key=True, index=True)
    container_id = Column(String, unique=True, index=True)
