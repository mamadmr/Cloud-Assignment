from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Container(Base):
    __tablename__ = 'containers'
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, index=True)
    challenge_id = Column(String, index=True)
    container_name = Column(String, unique=True)
    container_address = Column(String)
