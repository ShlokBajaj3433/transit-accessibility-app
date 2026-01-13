# backend/routes/climate.py
# Climate impact tracking and gamification endpoints

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.climate_service import ClimateEngine

router = APIRouter(prefix="/api", tags=["Impact Tracking"])

# Initialize Climate Engine for emissions tracking
climate_engine = ClimateEngine()


# Pydantic Models

class TripRequest(BaseModel):
    """Model for transit trip information"""
    distance_km: float = Field(..., gt=0, description="Distance traveled in kilometers")
    mode: str = Field(..., description="Transit mode: 'bus', 'walk', 'bike', 'subway', 'car'")


class ImpactResponse(BaseModel):
    """Response model for climate impact calculation"""
    mode: str
    distance_km: float
    baseline_car_kg: float = Field(..., description="CO2 emissions if traveled by car")
    actual_kg: float = Field(..., description="Actual CO2 emissions for selected mode")
    co2_saved_kg: float = Field(..., description="CO2 saved compared to driving")
    points_earned: int = Field(..., description="Gamification points earned")


# Routes

@router.post("/calculate-impact", response_model=ImpactResponse)
async def calculate_impact(trip: TripRequest):
    """
    Calculate environmental impact of a transit trip
    
    **Functionality:**
    - Compares emissions against baseline (driving a car)
    - Calculates CO2 saved by using sustainable transit
    - Awards gamification points
    
    **Parameters:**
    - distance_km: Trip distance in kilometers (must be positive)
    - mode: Transit mode (bus, walk, bike, subway, car)
    
    **Returns:**
    - CO2 metrics (baseline, actual, saved)
    - Gamification points earned
    
    **Example:**
    ```json
    {
        "distance_km": 5.0,
        "mode": "bus"
    }
    ```
    """
    # Validate input
    if trip.distance_km < 0:
        raise HTTPException(
            status_code=400,
            detail="Distance cannot be negative"
        )
    
    # Validate mode
    valid_modes = ["bus", "walk", "bike", "subway", "car"]
    if trip.mode.lower() not in valid_modes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mode. Must be one of: {', '.join(valid_modes)}"
        )
    
    # Calculate impact using climate engine
    result = climate_engine.calculate_savings(trip.distance_km, trip.mode)
    return result
