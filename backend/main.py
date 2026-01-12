# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.climate_service import ClimateEngine  # Importing your class

app = FastAPI(title="Inclusive Transit API")

# Initialize your engine
climate_engine = ClimateEngine()


# 1. Define the Input Format (Data Validation)
class TripRequest(BaseModel):
    distance_km: float
    mode: str  # "bus", "walk", "car", "subway"


# 2. Define the Route
@app.post("/api/calculate-impact")
async def calculate_impact(trip: TripRequest):
    """
    Frontend sends: {"distance_km": 5.0, "mode": "bus"}
    Backend returns: JSON with points and CO2 saved
    """
    if trip.distance_km < 0:
        raise HTTPException(status_code=400, detail="Distance cannot be negative")

    result = climate_engine.calculate_savings(trip.distance_km, trip.mode)
    return result


@app.get("/")
def home():
    return {"message": "Transit API is running! 🚀"}