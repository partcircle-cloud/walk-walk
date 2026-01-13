from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WalkCreate(BaseModel):
    duration: int
    distance: float
    steps: int

class WalkResponse(BaseModel):
    id: int
    date: datetime
    duration: int
    distance: float
    steps: int
    created_at: datetime

    class Config:
        from_attributes = True

class WeatherResponse(BaseModel):
    temp: float
    condition: str
    icon: str