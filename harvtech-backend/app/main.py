from fastapi import FastAPI

app = FastAPI(
    title="HarvTech Backend API",
    description="Backend API for the HarvTech Smart Agricultural Vehicle Monitoring System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to HarvTech Backend",
        "status": "Backend is running successfully!"
    }