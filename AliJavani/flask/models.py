#models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URI

Base = declarative_base()

class Container(Base):
    __tablename__ = 'containers'
    id = Column(Integer, primary_key=True)
    team_id = Column(String, nullable=False)
    challenge_id = Column(String, nullable=False)
    container_id = Column(String, nullable=False)
    address = Column(String, nullable=False)

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
