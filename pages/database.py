import streamlit as st
import pandas as pd
from src.utils import *

st.set_page_config(layout="wide")
st.title("Database")

load_all()

# Data editor
if not st.session_state.database.empty:
	st.session_state.database = st.data_editor(
		st.session_state.database,
		num_rows="dynamic",
		use_container_width=True,
		hide_index=True
	)

if st.button("Alles opslaan"):
	try:
		st.session_state.database.to_csv(FILE_PATH, index=False, sep=";")
		st.success("Bestand opgeslagen!")
	except Exception as e:
		st.error(f"Error bij bestand opslaan: {e}")