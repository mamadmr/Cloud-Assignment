from fastapi import FastAPI
from api.routes import router as assignment_router

application = FastAPI(title="Assignment Manager API")
application.include_router(assignment_router)
