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

st.write(available_rooms[50])

data_df = pd.DataFrame(
    {
        "rooms": [
            "Data Exploration",
            "Data Visualization",
            "LLM",
            "Data Exploration",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[
                "Data Exploration",
                "Data Visualization",
                "LLM",
            ],
            required=True,
        )
    },
    hide_index=True,
)

