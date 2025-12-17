# run with streamlit run your_script.py [-- script args]
import streamlit as st
import pandas as pd
import datetime
import requests
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="create")

#important!
# left, middle = st.columns(2)
# left.button("Say hello", type="secondary")

#Boolean for checking if there are any errors
errors = False

st.title("Select a room")

#try thing = st.header

st.header("Event information", divider=True)

name = st.text_input("Enter event name")

attendees = st.number_input("number of attendees", format="%1d", step=1)

#give error if 0
if attendees == 0:
    st.error("Please enter more then 0 attendees")
    errors = True

requiredEqiup = st.text_input("Enter required equipment")

startDate = st.date_input("Start date", datetime.date(2025, 6, 7))
endDate = st.date_input("End date", datetime.date(2026, 6, 7))




st.header("Available rooms", divider=True)

#this is placeholder
available_rooms = []

if available_rooms:
    option = st.selectbox(
        "Select an available room",
        available_rooms,
        format_func=lambda r: f"Room {r['id']} | cap: {r['capacity']} | {', '.join(r['equipments'])}"
    )

    df = pd.DataFrame(available_rooms)
    st.dataframe(df, use_container_width=True)


#st.write(available_rooms[50])

#event
#time
#capasity

option = st.selectbox(
    "Select an available room",
    available_rooms,
)

data_df = pd.DataFrame(
    {
        "Search availibility": available_rooms,
    }
)

st.data_editor(
    data_df,
    column_config={
        "Available rooms": st.column_config.NumberColumn(
            "Available rooms",
            help="The rooms available",
            min_value=0,
            max_value=1000,
            step=1,
            format="%d",
        )
    },
    hide_index=True,
    disabled=True,
)

left, right = st.columns(2)


if left.button("Go back", width="stretch", type='primary'):
    pass


if right.button("Continue", type="primary", width="stretch") and not errors and available_rooms:
    booking_payload = {
        "room_id": option["id"],
        "event_name": name,
        "attendees": int(attendees),
        "required_equipments": option["equipments"],
        "start_date": startDate.isoformat(),
        "end_date": endDate.isoformat(),
    }

    response = requests.post(
        f"{API_BASE}/bookings",
        json=booking_payload,
    )

    if response.status_code == 201:
        st.success("Booking created successfully")
        st.json(response.json())
    else:
        st.error(response.text)


