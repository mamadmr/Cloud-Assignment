from fastapi import FastAPI
from app.routers import challenge
from app.models import Base
from app.database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="CTF Challenge Manager",
    description="Manage CTF containers per team and challenge",
    version="1.0.0"
)

# Include your challenge router
app.include_router(challenge.router, prefix="/challenge", tags=["Challenges"])

