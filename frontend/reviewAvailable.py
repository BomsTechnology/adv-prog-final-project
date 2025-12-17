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

for i in range(20):
    available_rooms.append(i) 

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


right.button("continue", width="stretch")

