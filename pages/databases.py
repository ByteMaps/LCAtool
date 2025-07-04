import streamlit as st
import pandas as pd
from src.utils import *

st.set_page_config(layout="wide")
st.title("Databases")

# MATERIALS ========================================================================================================================================

st.subheader("Materials")
# Data editor
if not st.session_state.materials.empty:
	st.session_state.materials = st.data_editor(
		st.session_state.materials,
		num_rows="dynamic",
		use_container_width=True
	)

if st.button("Save Materials"):
	try:
		st.session_state.materials.to_csv(MATERIALS, index=False, sep=";")
		st.success("File saved successfully!")
	except Exception as e:
		st.error(f"Error saving file: {e}")

# TRANSPORT ========================================================================================================================================

st.subheader("Transport")
# Data editor
if not st.session_state.transport.empty:
	st.session_state.transport = st.data_editor(
		st.session_state.transport,
		num_rows="dynamic",
		use_container_width=True
	)

if st.button("Save Transport"):
	try:
		st.session_state.transport.to_csv(TRANSPORT, index=False, sep=";")
		st.success("File saved successfully!")
	except Exception as e:
		st.error(f"Error saving file: {e}")

# PROCESSES ========================================================================================================================================

st.subheader("Processes")
# Data editor
if not st.session_state.processes.empty:
	st.session_state.processes = st.data_editor(
		st.session_state.processes,
		num_rows="dynamic",
		use_container_width=True
	)

if st.button("Save Processes"):
	try:
		st.session_state.processes.to_csv(PROCESSES, index=False, sep=";")
		st.success("File saved successfully!")
	except Exception as e:
		st.error(f"Error saving file: {e}")