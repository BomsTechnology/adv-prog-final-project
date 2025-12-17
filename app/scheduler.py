from datetime import datetime
from typing import List, Optional
from models import Room, Event, Booking
from database import Database


class Scheduler:
    """Manages rooms, events, and bookings with database persistence."""
    
    def __init__(self, db_path: str = "booking_system.db"):
        self.db = Database(db_path)
        self.load_from_database()
    
    def load_from_database(self):
        """Load all data from the database."""
        self.rooms = self.db.get_all_rooms()
        self.events = self.db.get_all_events()
        self.bookings = self.db.get_all_bookings()
    
    def add_room(self, room: Room):
        """Add a room to the scheduler and save to database."""
        self.rooms.append(room)
        self.db.save_room(room)
        print(f"✓ Room '{room.name}' added")
    
    def add_event(self, event: Event):
        """Add an event to the scheduler and save to database."""
        self.events.append(event)
        self.db.save_event(event)
        print(f"✓ Event '{event.name}' added")
    
    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        """Find a room by its ID."""
        return next((r for r in self.rooms if r.id == room_id), None)
    
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Find an event by its ID."""
        return next((e for e in self.events if e.id == event_id), None)
    
    def find_available_rooms(self, event: Event, start_date: datetime, 
                            end_date: datetime) -> List[Room]:
        """Find all rooms that can accommodate the event and are available."""
        available_rooms = []
        
        for room in self.rooms:
            if not event.is_suitable_for_room(room):
                continue
            
            if self.is_room_available(room.id, start_date, end_date):
                available_rooms.append(room)
        
        return available_rooms
    
    def is_room_available(self, room_id: int, start_date: datetime, 
                         end_date: datetime, exclude_booking_id: int = None) -> bool:
        """Check if a room is available during a specific time period."""
        for booking in self.bookings:
            if booking.room_id != room_id:
                continue
            
            if exclude_booking_id and booking.id == exclude_booking_id:
                continue
            
            if start_date < booking.end_date and end_date > booking.start_date:
                return False
        
        return True
    
    def create_booking(self, room_id: int, event_name: str, attendees: int,
                      required_equipments: List[str], start_date: datetime, 
                      end_date: datetime) -> Optional[Booking]:
        """Create an event and booking together if the room is available."""
        room = self.get_room_by_id(room_id)
        
        if not room:
            print(f"Error: Room {room_id} not found")
            return None
        
        # Generate new event ID
        event_id = max([e.id for e in self.events], default=0) + 1
        
        # Create the event
        event = Event(event_id, event_name, attendees, required_equipments)
        
        # Validate room suitability
        if not event.is_suitable_for_room(room):
            print(f"Error: Room '{room.name}' is not suitable for '{event_name}'")
            if room.capacity < event.attendees:
                print(f"  - Capacity: {room.capacity} < {attendees} attendees")
            missing_eq = [eq for eq in required_equipments if eq not in room.equipments]
            if missing_eq:
                print(f"  - Missing equipment: {', '.join(missing_eq)}")
            return None
        
        # Check availability
        if not self.is_room_available(room_id, start_date, end_date):
            print(f"Error: Room '{room.name}' is not available during the requested time")
            return None
        
        # Save event to database
        self.events.append(event)
        self.db.save_event(event)
        
        # Create temporary booking with ID 0 (will be updated)
        booking = Booking(0, room_id, event_id, start_date, end_date)
        booking_id = self.db.save_booking(booking)
        booking.id = booking_id
        
        self.bookings.append(booking)
        print(f"✓ Booking #{booking_id} created: '{event_name}' in '{room.name}'")
        return booking
    
    def cancel_booking(self, booking_id: int) -> bool:
        """Cancel a booking by its ID."""
        booking = next((b for b in self.bookings if b.id == booking_id), None)
        if booking:
            self.bookings.remove(booking)
            self.db.delete_booking(booking_id)
            print(f"✓ Booking #{booking_id} cancelled")
            return True
        print(f"Error: Booking {booking_id} not found")
        return False
    
    def get_room_schedule(self, room_id: int, date: datetime = None) -> List[Booking]:
        """Get all bookings for a specific room, optionally filtered by date."""
        bookings = [b for b in self.bookings if b.room_id == room_id]
        
        if date:
            bookings = [b for b in bookings 
                       if b.start_date.date() == date.date()]
        
        return sorted(bookings, key=lambda b: b.start_date)
    
    def get_event_booking(self, event_id: int) -> Optional[Booking]:
        """Get the booking for a specific event."""
        return next((b for b in self.bookings if b.event_id == event_id), None)
    
    def print_schedule_summary(self):
        """Print a summary of all bookings."""
        print("\n" + "="*50)
        print("BOOKING SCHEDULE")
        print("="*50)
        
        if not self.bookings:
            print("No bookings scheduled.")
            return
        
        for booking in sorted(self.bookings, key=lambda b: b.start_date):
            room = self.get_room_by_id(booking.room_id)
            event = self.get_event_by_id(booking.event_id)
            print(f"\nBooking #{booking.id}")
            print(f"  Room: {room.name if room else 'Unknown'}")
            print(f"  Event: {event.name if event else 'Unknown'}")
            print(f"  Start: {booking.start_date.strftime('%Y-%m-%d %H:%M')}")
            print(f"  End: {booking.end_date.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Duration: {booking.duration_hours():.1f} hours")