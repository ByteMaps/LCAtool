import streamlit as st
import pandas as pd
import numpy as np
from src.utils import *
from uuid import uuid4

# SESSION ========================================================================================================================================

# Define a variable as a key
if 'dek' not in st.session_state:
    st.session_state.dek = str(uuid4())
if 'name' not in st.session_state:
    st.session_state.name = str(uuid4())
if 'type' not in st.session_state:
    st.session_state.type = str(uuid4())
if 'desc' not in st.session_state:
    st.session_state.desc = str(uuid4())

if "database" not in st.session_state or "client" not in st.session_state:
	st.session_state.client, st.session_state.database = load_database()

def update():
	# Change the key of the data editor to start over.
	st.session_state.dek = str(uuid4())
	st.session_state.name = str(uuid4())
	st.session_state.type = str(uuid4())
	st.session_state.desc = str(uuid4())


# SESSION ========================================================================================================================================

st.title("Nieuwe Data")

entrytype = st.toggle("Invoer uit Excel")

st.session_state.item = pd.DataFrame(columns=["Impact category", "Result"]) if not entrytype else pd.DataFrame(columns=["Impact category", "Reference unit", "Result"])

with st.form("newItem"):
	col1, col2, col3 = st.columns(3)
	with col1:
		name = st.text_input("Naam", key=st.session_state.name)
	with col2:
		item_type = st.selectbox("Item", options=st.session_state.database["itemtype"].unique(), accept_new_options=True, key=st.session_state.type)
	with col3:
		flow_type = st.selectbox("Flow", options=FLOWS)

	description = st.text_input("Beschrijving", key=st.session_state.desc)
			

	# Data editor
	st.write("Klik om een nieuwe rij aan te maken, CTRL+V daarna om data te plaatsen. Deze data staat geformatteerd in OpenLCA per proces/flow, of \
		  kan geëxporteerd worden uit Excel (check boven).")
	st.session_state.item = st.data_editor(
		st.session_state.item,
		num_rows="dynamic",
		use_container_width=True,
		key=st.session_state.dek
	)

	submitted = st.form_submit_button("Toevoegen")
	if submitted:
		add_to_db(name, item_type, flow_type, description, st.session_state.item, entrytype)
		update()
		st.success("Data toegevoegd!")

st.button("Wis Alles", on_click=update)