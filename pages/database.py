import streamlit as st
from src.utils import *
from uuid import uuid4

st.set_page_config(layout="wide")

# SESSION ========================================================================================================================================

if "database" not in st.session_state:
	st.session_state.client, st.session_state.database = load_database()

# SESSION ========================================================================================================================================

st.title("Database")

if 'nde' not in st.session_state:
    st.session_state.nde = str(uuid4())

if not st.session_state.database.empty:
	float_cols = st.session_state.database.select_dtypes(include=['float']).columns
	new_data = st.data_editor(
		st.session_state.database,
		num_rows="dynamic",
		use_container_width=True,
		column_config={c: st.column_config.NumberColumn(step=0.00001) for c in float_cols},
		hide_index=True,
		key=st.session_state.nde
	)

	col1, col2 = st.columns(2)

	with col1:
		if st.button("Opslaan"):
			try:
				new_data[float_cols] = new_data[float_cols].apply(to_numeric, errors='coerce')
				overwrite_db(new_data.to_dict(orient="records"), st.session_state.client)
				st.success("Data overgeschreven!")
			except Exception as e:
				st.error(f"Gefaald: {e}")

	with col2:
		if st.button("Opnieuw laden"):
			try:
				st.session_state.nde = str(uuid4())
			except Exception as e:
				st.error(f"Error bij opnieuw laden van database")