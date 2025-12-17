import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from app.models import Room, Event, Booking


class Database:
    """Handles all database operations for the booking system."""
    
    def __init__(self, db_path: str = "booking_system.db"):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def initialize_database(self):
        """Create tables if they don't exist."""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Create rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                equipments TEXT NOT NULL
            )
        ''')
        
        # Create events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                attendees INTEGER NOT NULL,
                required_equipments TEXT NOT NULL
            )
        ''')
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                event_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms (id),
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        ''')
        
        conn.commit()
        self.close()
    
    def save_room(self, room: Room):
        """Save or update a room in the database."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO rooms (id, name, capacity, equipments)
            VALUES (?, ?, ?, ?)
        ''', (room.id, room.name, room.capacity, json.dumps(room.equipments)))
        
        conn.commit()
        self.close()
    
    def save_event(self, event: Event):
        """Save or update an event in the database."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO events (id, name, attendees, required_equipments)
            VALUES (?, ?, ?, ?)
        ''', (event.id, event.name, event.attendees, json.dumps(event.required_equipments)))
        
        conn.commit()
        self.close()
    
    def save_booking(self, booking: Booking) -> int:
        """Save a booking in the database and return its ID."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bookings (room_id, event_id, start_date, end_date)
            VALUES (?, ?, ?, ?)
        ''', (booking.room_id, booking.event_id, 
              booking.start_date.isoformat(), booking.end_date.isoformat()))
        
        booking_id = cursor.lastrowid
        conn.commit()
        self.close()
        
        return booking_id
    
    def get_all_rooms(self) -> List[Room]:
        """Retrieve all rooms from the database."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM rooms')
        rows = cursor.fetchall()
        
        rooms = []
        for row in rows:
            rooms.append(Room(
                row['id'],
                row['name'],
                row['capacity'],
                json.loads(row['equipments'])
            ))
        
        self.close()
        return rooms
    
    def get_all_events(self) -> List[Event]:
        """Retrieve all events from the database."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM events')
        rows = cursor.fetchall()
        
        events = []
        for row in rows:
            events.append(Event(
                row['id'],
                row['name'],
                row['attendees'],
                json.loads(row['required_equipments'])
            ))
        
        self.close()
        return events
    
    def get_all_bookings(self) -> List[Booking]:
        """Retrieve all bookings from the database."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bookings')
        rows = cursor.fetchall()
        
        bookings = []
        for row in rows:
            bookings.append(Booking(
                row['id'],
                row['room_id'],
                row['event_id'],
                datetime.fromisoformat(row['start_date']),
                datetime.fromisoformat(row['end_date'])
            ))
        
        self.close()
        return bookings
    
    def delete_booking(self, booking_id: int) -> bool:
        """Delete a booking from the database."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        self.close()
        
        return deleted
    
    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        """Get a specific room by ID."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
        row = cursor.fetchone()
        
        self.close()
        
        if row:
            return Room(row['id'], row['name'], row['capacity'], 
                       json.loads(row['equipments']))
        return None
    
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get a specific event by ID."""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        
        self.close()
        
        if row:
            return Event(row['id'], row['name'], row['attendees'],
                        json.loads(row['required_equipments']))
        return None