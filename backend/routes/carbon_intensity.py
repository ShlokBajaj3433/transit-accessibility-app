from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Tuple

from services.carbon_intensity_service import init_db, lowest_intensity_times

router = APIRouter(prefix="/api/climate", tags=["Climate (Carbon Intensity)"])

class LowestIntensityItem(BaseModel):
    ts_utc: str
    carbon_gco2_per_kwh: float

@router.get("/lowest-intensity", response_model=List[LowestIntensityItem])
def get_lowest_intensity(
    location: str = Query(..., description="Location name, e.g. 'Toronto'"),
    limit: int = Query(5, ge=1, le=24, description="How many best hours to return")
):
    init_db()
    rows = lowest_intensity_times(location, limit=limit)
    return [{"ts_utc": ts, "carbon_gco2_per_kwh": val} for ts, val in rows]
