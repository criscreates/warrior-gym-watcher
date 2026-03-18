from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional


class OccupancyBase(BaseModel):
    count: int = Field(ge=0, description="Current number of occupants")
    percent: int = Field(ge=0, le=100, description="Occupancy %")
    capacity: int = Field(ge=0, description="Calculated total capacity")


class OccupancyCreate(OccupancyBase):
    facility_name: str  # using name to lookup DB ID


class OccupancyRead(OccupancyBase):
    id: int
    facility_id: int
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FacilityBase(BaseModel):
    name: str = Field(..., min_length=3)


class FacilityCreate(FacilityBase):
    pass


class FacilityRead(FacilityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
