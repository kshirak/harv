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


@app.get("/dashboard")
def get_dashboard_page():
    return {
        "page": "dashboard",
        "title": "Dashboard",
        "widgets": [
            {"name": "Vehicle Status", "value": "Online"},
            {"name": "Active Alerts", "value": 2},
        ],
    }


@app.get("/gps-map")
def get_gps_map_page():
    return {
        "page": "gps-map",
        "title": "GPS Map",
        "vehicles": [
            {"id": "V-1001", "latitude": 11.0168, "longitude": 76.9558, "status": "Moving"},
            {"id": "V-1002", "latitude": 11.0182, "longitude": 76.9584, "status": "Idle"},
        ],
    }


@app.get("/diagnostics")
def get_diagnostics_page():
    return {
        "page": "diagnostics",
        "title": "Diagnostics",
        "systems": [
            {"name": "Engine", "status": "Healthy"},
            {"name": "Fuel", "status": "Needs Check"},
        ],
    }


@app.get("/")
def root():
    return {
        "message": "Welcome to HarvTech Backend",
        "status": "Backend is running successfully!"
    }