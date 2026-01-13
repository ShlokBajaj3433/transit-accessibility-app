# backend/routes/routing.py
# Route planning endpoints

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter(prefix="/api", tags=["Route Planning"])


# Pydantic Models

class RouteOption(BaseModel):
    """Model for a single transit route option"""
    route_id: str
    origin: str
    destination: str
    mode: str
    estimated_time_minutes: int
    stops_count: int
    accessibility_score: float = Field(..., ge=0, le=100, description="0-100 accessibility rating")
    has_elevator: bool
    wheelchair_accessible: bool
    audio_assistance_available: bool


# Routes

@router.post("/route/plan", response_model=List[RouteOption])
async def plan_accessible_route(
    origin: str = Query(..., description="Starting location"),
    destination: str = Query(..., description="Destination location"),
    accessibility_priority: Optional[str] = Query(
        "balanced",
        description="'accessibility' or 'time' - determines route optimization"
    )
):
    """
    Plan a transit route with accessibility considerations
    
    **Functionality:**
    - Generates multiple route options for origin to destination
    - Prioritizes accessibility features (elevators, wheelchair access, audio guides)
    - Considers user's accessibility needs
    - Provides real-time transit information
    
    **Parameters:**
    - origin: Starting location/address
    - destination: End location/address
    - accessibility_priority: 'accessibility' (default) or 'time'
    
    **Returns:**
    - List of route options with:
      - Estimated travel time
      - Accessibility scores (0-100)
      - Available accessibility features
      - Number of stops
    
    **Note:** Currently returns mock data. To be integrated with transit APIs.
    """
    # TODO: Integrate with transit routing engine (GTFS, Google Transit API, etc.)
    mock_routes = [
        RouteOption(
            route_id="route_001",
            origin=origin,
            destination=destination,
            mode="bus",
            estimated_time_minutes=25,
            stops_count=5,
            accessibility_score=95.0,
            has_elevator=True,
            wheelchair_accessible=True,
            audio_assistance_available=True
        ),
        RouteOption(
            route_id="route_002",
            origin=origin,
            destination=destination,
            mode="subway",
            estimated_time_minutes=15,
            stops_count=3,
            accessibility_score=85.0,
            has_elevator=True,
            wheelchair_accessible=True,
            audio_assistance_available=False
        )
    ]
    
    return mock_routes
