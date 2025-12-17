from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
from typing import List
from app.schemas import AvailabilityCheck, BookingResponse, RoomCreate, RoomResponse, BookingCreate
from app.scheduler import Scheduler
from app.models import Room, Event, Booking

app = FastAPI(title="Booking System API", version="1.0.0")

# CORS pour permettre les appels depuis un frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser le scheduler
scheduler = Scheduler("booking_system.db")




# ==================== Room Endpoints ====================

@app.post("/rooms", response_model=RoomResponse, status_code=201)
def create_room(room: RoomCreate):
    """Créer une nouvelle salle"""
    try:
        new_room = Room(room.id, room.name, room.capacity, room.equipments)
        scheduler.add_room(new_room)
        return room.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/rooms", response_model=List[RoomResponse])
def get_all_rooms():
    """Récupérer toutes les salles"""
    rooms = scheduler.get_all_rooms()
    return [
        {
            "id": r.id,
            "name": r.name,
            "capacity": r.capacity,
            "equipments": r.equipments
        }
        for r in rooms
    ]

@app.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: int):
    """Récupérer une salle spécifique"""
    room = scheduler.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
    return {
        "id": room.id,
        "name": room.name,
        "capacity": room.capacity,
        "equipments": room.equipments
    }

@app.delete("/rooms/{room_id}", status_code=204)
def delete_room(room_id: int):
    """Supprimer une salle"""
    try:
        scheduler.delete_room(room_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== Booking Endpoints ====================

@app.post("/bookings", response_model=BookingResponse, status_code=201)
def create_booking(booking: BookingCreate):
    """Créer une nouvelle réservation"""
    try:
        new_booking = scheduler.create_booking(
            room_id=booking.room_id,
            event_name=booking.event_name,
            attendees=booking.attendees,
            required_equipments=booking.required_equipments,
            start_date=booking.start_date,
            end_date=booking.end_date
        )
        return {
            "id": new_booking.id,
            "room_id": new_booking.room_id,
            "event_id": new_booking.event_id,
            "start_date": new_booking.start_date,
            "end_date": new_booking.end_date,
            "duration_hours": new_booking.duration_hours
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/bookings", response_model=List[BookingResponse])
def get_all_bookings():
    """Récupérer toutes les réservations"""
    bookings = scheduler.get_all_bookings()
    return [
        {
            "id": b.id,
            "room_id": b.room_id,
            "event_id": b.event_id,
            "start_date": b.start_date,
            "end_date": b.end_date,
            "duration_hours": b.duration_hours
        }
        for b in bookings
    ]

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int):
    """Récupérer une réservation spécifique"""
    booking = scheduler.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    return {
        "id": booking.id,
        "room_id": booking.room_id,
        "event_id": booking.event_id,
        "start_date": booking.start_date,
        "end_date": booking.end_date,
        "duration_hours": booking.duration_hours
    }

@app.delete("/bookings/{booking_id}", status_code=204)
def cancel_booking(booking_id: int):
    """Annuler une réservation"""
    if not scheduler.cancel_booking(booking_id):
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")

@app.get("/rooms/{room_id}/bookings", response_model=List[BookingResponse])
def get_room_bookings(room_id: int):
    """Récupérer toutes les réservations d'une salle"""
    bookings = scheduler.get_room_bookings(room_id)
    return [
        {
            "id": b.id,
            "room_id": b.room_id,
            "event_id": b.event_id,
            "start_date": b.start_date,
            "end_date": b.end_date,
            "duration_hours": b.duration_hours
        }
        for b in bookings
    ]

# ==================== Availability Endpoints ====================

@app.post("/availability/check")
def check_availability(availability: AvailabilityCheck):
    """Vérifier les salles disponibles pour un événement"""
    event = Event(
        id=0,  # Temporaire
        name=availability.event_name,
        attendees=availability.attendees,
        required_equipments=availability.required_equipments
    )
    
    available_rooms = scheduler.find_available_rooms(
        event,
        availability.start_date,
        availability.end_date
    )
    
    return {
        "available": len(available_rooms) > 0,
        "rooms": [
            {
                "id": r.id,
                "name": r.name,
                "capacity": r.capacity,
                "equipments": r.equipments
            }
            for r in available_rooms
        ]
    }

@app.get("/rooms/{room_id}/availability")
def check_room_availability(
    room_id: int,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...)
):
    """Vérifier si une salle est disponible pour une période donnée"""
    is_available = scheduler.is_room_available(room_id, start_date, end_date)
    return {
        "room_id": room_id,
        "start_date": start_date,
        "end_date": end_date,
        "available": is_available
    }

# ==================== Schedule Endpoints ====================

@app.get("/rooms/{room_id}/schedule")
def get_room_schedule(room_id: int):
    """Récupérer le planning d'une salle"""
    bookings = scheduler.get_room_schedule(room_id)
    room = scheduler.get_room(room_id)
    
    if not room:
        raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
    
    return {
        "room": {
            "id": room.id,
            "name": room.name,
            "capacity": room.capacity,
            "equipments": room.equipments
        },
        "bookings": [
            {
                "id": b.id,
                "event_id": b.event_id,
                "start_date": b.start_date,
                "end_date": b.end_date,
                "duration_hours": b.duration_hours
            }
            for b in bookings
        ]
    }

# ==================== Health Check ====================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Booking System API is running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Vérifier l'état de l'API et de la base de données"""
    try:
        # Test de connexion à la base de données
        rooms = scheduler.get_all_rooms()
        return {
            "status": "healthy",
            "database": "connected",
            "total_rooms": len(rooms)
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")