import streamlit as st
import pandas as pd
from src.utils import *
from uuid import uuid4

st.set_page_config(layout="wide")

# SESSION ========================================================================================================================================

if 'database' not in st.session_state: # TODO change loaded
	st.session_state.database = load_all()

# SESSION ========================================================================================================================================

st.title("Database")

if 'nde' not in st.session_state:
    st.session_state.nde = str(uuid4())

# Data editor
if not st.session_state.database.empty:					# TODO change database
	st.session_state.database = st.data_editor(
		st.session_state.database,
		num_rows="dynamic",
		use_container_width=True,
		hide_index=True,
		key=st.session_state.nde
	)

col1, col2 = st.columns(2)

with col1:
	if st.button("Alles opslaan"):
		try:
			st.session_state.database.to_csv(FILE_PATH, index=False, sep=";")	# TODO change func
			st.success("Bestand opgeslagen!")
		except Exception as e:
			st.error(f"Error bij bestand opslaan: {e}")

with col2:
	if st.button("Opnieuw laden"):
		try:
			st.session_state.nde = str(uuid4())
		except Exception as e:
			st.error(f"Error bij opnieuw laden van database")