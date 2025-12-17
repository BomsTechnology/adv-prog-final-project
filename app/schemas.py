from pydantic import BaseModel
from typing import List
from datetime import datetime

class RoomCreate(BaseModel):
    id: int
    name: str
    capacity: int
    equipments: List[str]

class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    equipments: List[str]

class EventCreate(BaseModel):
    name: str
    attendees: int
    required_equipments: List[str]

class BookingCreate(BaseModel):
    room_id: int
    event_name: str
    attendees: int
    required_equipments: List[str]
    start_date: datetime
    end_date: datetime

class BookingResponse(BaseModel):
    id: int
    room_id: int
    event_id: int
    start_date: datetime
    end_date: datetime
    duration_hours: float

class AvailabilityCheck(BaseModel):
    event_name: str
    attendees: int
    required_equipments: List[str]
    start_date: datetime
    end_date: datetime