# run with streamlit run your_script.py [-- script args]
import streamlit as st
import pandas as pd

#important!
# left, middle = st.columns(2)
# left.button("Say hello", type="secondary")

st.title("Select a room")
st.header("Available rooms", divider=True)

#this is placeholder
available_rooms = []

for i in range(100):
    available_rooms.append(i) 

#st.write(available_rooms[50])

#event
#time
#capasity

data_df = pd.DataFrame(
    {
        "price": available_rooms,
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

