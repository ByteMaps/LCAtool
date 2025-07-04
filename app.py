import streamlit as st
from src.utils import *

st.title("LCA Tool voor verzorgend wassen")
if "form1_submitted" not in st.session_state:
	st.session_state.form1_submitted = False

# Selecting the materials and transport types from the loaded objects

with st.form("elementcheck"):
	st.write("Kies de elementen")

	materialcheck = st.checkbox('Materials')
	transportcheck = st.checkbox('Transport')
	processescheck = st.checkbox('Processes')

	flows = st.multiselect('Flows', options=FLOWS)

	# Submit button
	submitted = st.form_submit_button("Submit")
	if submitted:
		st.session_state.form1_submitted = True
		load_all()																		# TODO fix later based on selection
		st.session_state.flows = flows


