from sqlalchemy import Column, Integer, String
from config.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    docker_image = Column(String)
    container_port = Column(Integer)  