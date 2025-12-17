from datetime import datetime
from typing import List


class Room:
    """Represents a room with capacity and equipment."""
    
    def __init__(self, id: int, name: str, capacity: int, equipments: List[str]):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.equipments = equipments
    
    def has_equipment(self, equipment: str) -> bool:
        """Check if room has specific equipment."""
        return equipment in self.equipments
    
    def has_all_equipment(self, required_equipments: List[str]) -> bool:
        """Check if room has all required equipment."""
        return all(eq in self.equipments for eq in required_equipments)
    
    def __str__(self):
        return f"Room {self.id}: {self.name} (Capacity: {self.capacity})"
    
    def __repr__(self):
        return f"Room(id={self.id}, name='{self.name}', capacity={self.capacity}, equipments={self.equipments})"


class Event:
    """Represents an event with attendees and equipment requirements."""
    
    def __init__(self, id: int, name: str, attendees: int, required_equipments: List[str]):
        self.id = id
        self.name = name
        self.attendees = attendees
        self.required_equipments = required_equipments
    
    def is_suitable_for_room(self, room: Room) -> bool:
        """Check if the event can be held in the given room."""
        has_capacity = room.capacity >= self.attendees
        has_equipment = room.has_all_equipment(self.required_equipments)
        return has_capacity and has_equipment
    
    def __str__(self):
        return f"Event {self.id}: {self.name} ({self.attendees} attendees)"
    
    def __repr__(self):
        return f"Event(id={self.id}, name='{self.name}', attendees={self.attendees}, required_equipments={self.required_equipments})"


class Booking:
    """Represents a booking linking a room to an event for a time period."""
    
    def __init__(self, id: int, room_id: int, event_id: int, 
                 start_date: datetime, end_date: datetime):
        self.id = id
        self.room_id = room_id
        self.event_id = event_id
        self.start_date = start_date
        self.end_date = end_date
        
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
    
    def overlaps_with(self, other_booking: 'Booking') -> bool:
        """Check if this booking overlaps with another booking."""
        if self.room_id != other_booking.room_id:
            return False
        
        return (self.start_date < other_booking.end_date and 
                self.end_date > other_booking.start_date)
    
    def duration_hours(self) -> float:
        """Calculate booking duration in hours."""
        delta = self.end_date - self.start_date
        return delta.total_seconds() / 3600
    
    def __str__(self):
        return f"Booking {self.id}: Room {self.room_id} for Event {self.event_id}"
    
    def __repr__(self):
        return (f"Booking(id={self.id}, room_id={self.room_id}, "
                f"event_id={self.event_id}, start_date={self.start_date}, "
                f"end_date={self.end_date})")