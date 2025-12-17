"""
main.py - Main entry point for the booking system
"""
from datetime import datetime
from models import Room, Event
from scheduler import Scheduler


def initialize_sample_data(scheduler: Scheduler):
    """Initialize the database with sample rooms if empty."""
    if not scheduler.rooms:
        print("Initializing database with sample data...\n")
        scheduler.add_room(Room(1, "Conference Room A", 50, 
                               ["projector", "whiteboard", "microphone"]))
        scheduler.add_room(Room(2, "Meeting Room B", 10, 
                               ["whiteboard", "TV"]))
        scheduler.add_room(Room(3, "Auditorium", 200, 
                               ["projector", "microphone", "sound_system"]))


def main():
    """Main application logic."""
    print("="*60)
    print("BOOKING SYSTEM WITH SQLite")
    print("="*60)
    print()
    
    # Initialize scheduler (creates database if it doesn't exist)
    scheduler = Scheduler("booking_system.db")
    
    # Initialize sample data if needed
    initialize_sample_data(scheduler)
    
    # Show loaded data
    print(f"\nLoaded from database:")
    print(f"  - {len(scheduler.rooms)} rooms")
    print(f"  - {len(scheduler.events)} events")
    print(f"  - {len(scheduler.bookings)} existing bookings")
    
    # Create new bookings (event is created at the same time)
    print("\n" + "="*60)
    print("CREATING NEW BOOKINGS")
    print("="*60 + "\n")
    
    booking1 = scheduler.create_booking(
        room_id=1,
        event_name="Product Launch",
        attendees=45,
        required_equipments=["projector", "microphone"],
        start_date=datetime(2024, 12, 20, 9, 0),
        end_date=datetime(2024, 12, 20, 11, 0)
    )
    
    booking2 = scheduler.create_booking(
        room_id=2,
        event_name="Team Meeting",
        attendees=8,
        required_equipments=["whiteboard"],
        start_date=datetime(2024, 12, 20, 10, 0),
        end_date=datetime(2024, 12, 20, 11, 0)
    )
    
    # Try to double-book (should fail)
    print("\n" + "="*60)
    print("TESTING CONFLICT DETECTION")
    print("="*60 + "\n")
    
    booking3 = scheduler.create_booking(
        room_id=1,
        event_name="Training Session",
        attendees=15,
        required_equipments=["projector"],
        start_date=datetime(2024, 12, 20, 10, 0),  # Overlaps with booking1
        end_date=datetime(2024, 12, 20, 12, 0)
    )
    
    # Find available rooms
    print("\n" + "="*60)
    print("FINDING AVAILABLE ROOMS")
    print("="*60 + "\n")
    
    # Create a test event to find available rooms
    test_event = Event(999, "Workshop", 15, ["projector"])
    available = scheduler.find_available_rooms(
        test_event,
        datetime(2024, 12, 20, 14, 0),
        datetime(2024, 12, 20, 16, 0)
    )
    print(f"Available rooms for '{test_event.name}': {[r.name for r in available]}")
    
    # Print full schedule
    scheduler.print_schedule_summary()
    
    print("\n" + "="*60)
    print(f"Database saved to: booking_system.db")
    print("="*60)


if __name__ == "__main__":
    main()