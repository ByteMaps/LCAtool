import streamlit as st
from src.utils import *
from dotenv import load_dotenv

load_database()

# SESSION ========================================================================================================================================

if "form1_submitted" not in st.session_state:
	st.session_state.form1_submitted = False

if "database" not in st.session_state or "client" not in st.session_state:
	st.session_state.client, st.session_state.database = load_database()
# SESSION ========================================================================================================================================

st.title("LCA Tool voor verzorgend wassen")
st.markdown("Welkom bij de LCA tool, gebouwd door Bytemaps Consulting! Deze simpele tool analyseert de impact van een product systeem volgens de ILCD Impact Assessment"
"method (2011, midpoint) zoals direct geëxporteerd uit de ELCD database, OpenLCA. Voor het gebruik, voeg nieuwe impact waarden toe in het tabblad *new*, bewerk de database in *database* en analyseer de resultaten in *results*. ")