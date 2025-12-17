import streamlit as st
from datetime import time

#sample data
rooms = [
    {"id": "R101", "capacity": 40, "equipment": ["projector", "whiteboard"]},
    {"id": "R202", "capacity": 25, "equipment": ["whiteboard"]},
    {"id": "R303", "capacity": 60, "equipment": ["projector"]}
]

bookings = [
    {
        "room_id": "R101",
        "event": "Coding Club",
        "start": time(10, 0),
        "end": time(12, 0)
    },
    {
        "room_id": "R202",
        "event": "Math Society",
        "start": time(11, 0),
        "end": time(13, 0)
    }
]



st.set_page_config(page_title="Smart Campus Scheduler", layout="wide")
st.title("Smart Campus Event Scheduler", text_alignment="center")

st.subheader("Rooms Currently Booked", text_alignment="center")

if not bookings:
    st.success("All rooms are currently available")
else:
    for booking in bookings:
        room = next(r for r in rooms if r["id"] == booking["room_id"])

        with st.container(border=True):
            st.markdown(f"### {booking['event'].upper()}")
            st.write(f"**Room:** {room['id']}")
            st.write(f"**Time:** {booking['start']} – {booking['end']}")
            st.write(f"**Capacity:** {room['capacity']}")
            st.write(f"**Equipment:** {', '.join(room['equipment'])}")


if st.button("Book a Room"):
    st.session_state.page = ("reviewAvailable.py")