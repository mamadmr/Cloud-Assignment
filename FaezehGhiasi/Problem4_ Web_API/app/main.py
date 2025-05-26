from fastapi import FastAPI
from api import router as challenge_router

app = FastAPI(title="CTF Manager API")
app.include_router(challenge_router)
