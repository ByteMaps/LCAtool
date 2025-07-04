import streamlit as st
import pandas as pd
import numpy as np
from src.utils import *
import uuid

# SETUP ========================================================================================================================================
st.title("Nieuwe Data")
# Initialize session state

# Define a variable as a key
if 'dek' not in st.session_state:
    st.session_state.dek = str(uuid.uuid4())
if 'name' not in st.session_state:
    st.session_state.name = str(uuid.uuid4())
if 'type' not in st.session_state:
    st.session_state.type = str(uuid.uuid4())
if 'desc' not in st.session_state:
    st.session_state.desc = str(uuid.uuid4())

# FUNCTIONS ========================================================================================================================================

def update():
	# Change the key of the data editor to start over.
	st.session_state.dek = str(uuid.uuid4())
	st.session_state.name = str(uuid.uuid4())
	st.session_state.type = str(uuid.uuid4())
	st.session_state.desc = str(uuid.uuid4())

# LAYOUT ========================================================================================================================================

st.session_state.item = pd.DataFrame(columns=["Impact category", "Reference unit", "Result"])

with st.form("newItem"):
	col1, col2, col3 = st.columns(3)
	with col1:
		name = st.text_input("Naam", key=st.session_state.name)
	with col2:
		item_type = st.selectbox("Type", options=["Materiaal", "Transport", "Proces"], key=st.session_state.type)			# TODO voeg toe aan db gebaseerd op type
	with col3:
		flow_type = st.selectbox("Flow", options=FLOWS)

	description = st.text_input("Beschrijving", key=st.session_state.desc)
		
	# Data editor
	st.write("Klik om een nieuwe rij aan te maken, CTRL+V daarna om data te plaatsen")
	st.session_state.item = st.data_editor(
		st.session_state.item,
		num_rows="dynamic",
		use_container_width=True,
		key=st.session_state.dek
	)

	submitted = st.form_submit_button("Toevoegen")
	if submitted:
		update()
		st.success("Data toegevoegd!")
		print(st.session_state.item)

st.button("Wis Alles", on_click=update())
