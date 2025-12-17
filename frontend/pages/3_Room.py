import streamlit as st
import time
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Rooms")
def fetch_rooms():
    """Récupérer toutes les salles depuis l'API"""
    try:
        response = requests.get(f"{API_URL}/rooms")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des salles : {e}")
        return []
    
def fetch_room_schedule(room_id):
    """Récupérer le planning d'une salle"""
    try:
        response = requests.get(f"{API_URL}/rooms/{room_id}/schedule")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération du planning : {e}")
        return None
    
@st.dialog("Add room")
def room():
    st.write("Add new room")
    with st.form("add_room_form"):

        room_name = st.text_input("Nom", placeholder="Ex: Salle A")
    
        capacity = st.number_input("Capacité", min_value=1, value=10)
            
        equipments_input = st.multiselect(
            "Équipements",
            ["projector", "whiteboard", "tv", "videoconference", "wifi", "computer"],
            default=[]
        )
            
        custom_eq = st.text_input("Autres équipements (séparés par virgules)")
        
        if st.form_submit_button("Ajouter", type="primary"):
            equipments = equipments_input.copy()
            if custom_eq:
                equipments.extend([eq.strip() for eq in custom_eq.split(",") if eq.strip()])
            
            try:
                data = {
                    "name": room_name,
                    "capacity": int(capacity),
                    "equipments": equipments
                }
                response = requests.post(f"{API_URL}/rooms", json=data)
                response.raise_for_status()
                st.success(f"✅ Salle '{room_name}' créée !")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur : {e}")

st.markdown("# Rooms")
st.sidebar.header("Plotting Demo")
st.write(
    """All rooms are listed below."""
)
st.button("Refresh")

if "room" not in st.session_state:
    if st.button("Add room"):
        room()

rooms = fetch_rooms()



if rooms:
        # Affichage en colonnes
        cols = st.columns(3)
        
        for idx, room in enumerate(rooms):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.subheader(f"🚪 {room['name']}")
                    st.write(f"**Capacité :** {room['capacity']} personnes")
                    st.write(f"**Équipements :**")
                    if room['equipments']:
                        for eq in room['equipments']:
                            st.write(f"  • {eq}")
                    else:
                        st.write("  • Aucun")
                    
                    # Bouton pour voir le planning
                    if st.button(f"Voir planning", key=f"schedule_{room['id']}"):
                        st.session_state['view_schedule_room'] = room['id']
        
        # Afficher le planning si demandé
        if 'view_schedule_room' in st.session_state:
            room_id = st.session_state['view_schedule_room']
            st.divider()
            st.subheader(f"Planning de la salle #{room_id}")
            
            schedule = fetch_room_schedule(room_id)
            if schedule and schedule['bookings']:
                df = pd.DataFrame(schedule['bookings'])
                df['start_date'] = pd.to_datetime(df['start_date'])
                df['end_date'] = pd.to_datetime(df['end_date'])
                df = df[['id', 'start_date', 'end_date', 'duration_hours']]
                df.columns = ['ID', 'Début', 'Fin', 'Durée (h)']
                st.dataframe(df)
            else:
                st.info("Aucune réservation pour cette salle")
            
            if st.button("Fermer"):
                del st.session_state['view_schedule_room']
                st.rerun()
        
        
else:
    st.warning("Aucune salle disponible")



