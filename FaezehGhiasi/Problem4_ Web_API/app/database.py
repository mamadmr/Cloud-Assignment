from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://FaezehGhiasi:1234@db:5432/ctfdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class AssignedChallenge(Base):
    __tablename__ = "assigned_challenges"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, index=True)
    challenge_id = Column(Integer, index=True)
    container_name = Column(String, index=True)
    container_address = Column(String)
    status = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
