import streamlit as st
from src.utils import *

st.title("LCA Tool voor verzorgend wassen")
st.text("Welkom bij de LCA tool, gebouwd door Bytemaps Consulting! Deze simpele tool analyseert de impact van een product systeem volgens de ILCD Impact Assessment"
"method (2011, midpoint). Voor het gebruik, voeg nieuwe impact waarden toe in het tabblad 'new', bewerk de database in 'database' en analyseer de resultaten in 'results'. Succes!")
if "form1_submitted" not in st.session_state:
	st.session_state.form1_submitted = False

# Selecting the materials and transport types from the loaded objects

with st.form("elementcheck"):
	st.text("Deze inputs zijn nog niet in gebruik")
	col1, col2 = st.columns(2)
	with col1:
		flows = st.multiselect('Flows', options=FLOWS)
	with col2:
		itemtypes = st.multiselect('Types', options=TYPES)

	# Submit button
	submitted = st.form_submit_button("Submit")
	if submitted:
		st.session_state.form1_submitted = True
		st.session_state.flows = flows


