import streamlit as st
import pandas as pd
import numpy as np
from src.utils import *
import uuid

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

def save_to_csv(name, type, description, df):
	"""Save the form data to CSV"""
	pass

def update():
	# Change the key of the data editor to start over.
	st.session_state.dek = str(uuid.uuid4())
	st.session_state.name = str(uuid.uuid4())
	st.session_state.type = str(uuid.uuid4())
	st.session_state.desc = str(uuid.uuid4())
   
st.session_state.item = pd.DataFrame(columns=["Impact Name", "Reference unit", "Result"])

with st.form("newItem"):
	col1, col2 = st.columns(2)

	with col1:
		name = st.text_input("Naam", key=st.session_state.name)

	with col2:
		item_type = st.selectbox("Type", options=["Materiaal", "Transport", "Proces"], key=st.session_state.type)

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
