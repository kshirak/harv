from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers import auth as auth_router

app = FastAPI(
    title="HarvTech Backend API",
    description="Backend API for the HarvTech Smart Agricultural Vehicle Monitoring System",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to HarvTech Backend",
        "status": "Backend is running successfully!"
    }