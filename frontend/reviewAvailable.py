# run with streamlit run your_script.py [-- script args]
import streamlit as st
import pandas as pd
import datetime

#important!
# left, middle = st.columns(2)
# left.button("Say hello", type="secondary")

st.title("Select a room")

#try thing = st.header

st.header("Student information", divider=True)

name = st.text_input("Enter student name")

attendees = st.number_input("number of attendees", format="%1d", step=1)
if attendees == 0:
    st.error("Please enter more then 0 attendees")

requiredEqiup = st.text_input("Enter required equipment")

startDate = st.date_input("Start date", datetime.date(2025, 6, 7))
endDate = st.date_input("End date", datetime.date(2026, 6, 7))




st.header("Available rooms", divider=True)

#this is placeholder
available_rooms = []

for i in range(99):
    available_rooms.append(i+1) 

#st.write(available_rooms[50])

#event
#time
#capasity

data_df = pd.DataFrame(
    {
        "available rooms": available_rooms,
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
)

left, right = st.columns(2)

left.button("Go back", width="stretch", type='primary')
right.button("continue", width="stretch")

