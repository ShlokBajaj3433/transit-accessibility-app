# backend/routes/accessibility.py
# Accessibility information and alerts endpoints

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter(prefix="/api", tags=["Accessibility"])


# Pydantic Models

class AccessibilityFeature(BaseModel):
    """Model for accessibility information at a transit location"""
    feature_id: str
    feature_name: str
    is_available: bool
    description: Optional[str] = None


class StationAccessibilityInfo(BaseModel):
    """Model for complete accessibility info at a transit station/stop"""
    station_id: str
    station_name: str
    features: List[AccessibilityFeature]
    wheelchair_accessible: bool
    audio_announcements: bool
    visual_displays: bool
    elevators_working: bool
    accessible_restrooms: bool


# Routes

@router.get(
    "/station/{station_id}/accessibility",
    response_model=StationAccessibilityInfo
)
async def get_station_accessibility(station_id: str):
    """
    Retrieve accessibility information for a transit station
    
    **Functionality:**
    - Provides comprehensive accessibility features
    - Supports wheelchair users, visually impaired, hearing impaired
    - Real-time status of accessibility infrastructure
    
    **Parameters:**
    - station_id: Unique identifier for the transit station
    
    **Returns:**
    - Station name and location
    - List of available accessibility features
    - Status of elevators, restrooms, audio/visual systems
    
    **Note:** Currently returns mock data. To be integrated with database.
    """
    # TODO: Replace with actual database query
    mock_data = {
        "station_id": station_id,
        "station_name": f"Station {station_id}",
        "features": [
            AccessibilityFeature(
                feature_id="elevator_1",
                feature_name="Main Entrance Elevator",
                is_available=True,
                description="Accessible elevator with audio and Braille buttons"
            ),
            AccessibilityFeature(
                feature_id="ramp_1",
                feature_name="Wheelchair Ramp",
                is_available=True,
                description="Gentle slope ramp meeting ADA standards"
            )
        ],
        "wheelchair_accessible": True,
        "audio_announcements": True,
        "visual_displays": True,
        "elevators_working": True,
        "accessible_restrooms": True
    }
    return mock_data


@router.get("/alerts")
async def get_accessibility_alerts(
    station_id: Optional[str] = Query(None, description="Filter alerts by station ID")
):
    """
    Retrieve real-time accessibility alerts
    
    **Functionality:**
    - Provides alerts about broken elevators, accessibility issues
    - Helps users plan routes around inaccessible areas
    - Updates in real-time
    
    **Parameters:**
    - station_id (optional): Filter to specific station
    
    **Returns:**
    - List of active accessibility alerts with severity level
    
    **Note:** Currently returns mock data. To be integrated with real-time system.
    """
    # TODO: Integrate with real-time alert system
    mock_alerts = [
        {
            "alert_id": "alert_001",
            "station_id": "stn_downtown",
            "station_name": "Downtown Station",
            "severity": "high",
            "message": "Main elevator out of service for maintenance",
            "affected_accessibility": ["wheelchair", "mobility_impaired"],
            "estimated_resolution_time": "2 hours"
        }
    ]
    
    # Filter by station if provided
    if station_id:
        mock_alerts = [a for a in mock_alerts if a["station_id"] == station_id]
    
    return {"alerts": mock_alerts, "total_alerts": len(mock_alerts)}
