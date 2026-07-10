from pydantic import BaseModel, Field
from typing import Literal

class FlightInferenceInput(BaseModel):
    airline: str
    source_city: str
    departure_time: str
    stops: int = Field(..., ge=0, le=4)
    arrival_time: str
    destination_city: str
    class_type: str
    days_left: int = Field(..., gt=0, le=365)