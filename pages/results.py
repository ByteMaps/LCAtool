import streamlit as st
from src.utils import *

# SESSION ========================================================================================================================================

if 'database' not in st.session_state:
	st.session_state.database = load_all()

# SESSION ========================================================================================================================================

st.session_state.comparison = st.multiselect('Items om te vergelijken', options = st.session_state.database["itemtype"].unique())

for item in st.session_state.comparison:
	with st.form(f"{item}"):				# TODO add reset button
		st.subheader(f"{item}")
		col1, col2 = st.columns(2)
		with col1:
			re_use = st.slider('Keren hergebruik', 0, 100, 10, 1)
			quantity_multiplier = st.slider('Aantal gebruikseenheden', 1, 100, 1, 1)
		with col2:
			flowtypes = st.multiselect('Flow types', options = st.session_state.database["flowtype"].unique())
		submitted = st.form_submit_button("Maak")
		if submitted:
			results = calculate_impacts(st.session_state.database.copy(), item, quantity_multiplier, re_use, flowtypes)
			st.plotly_chart(impact_assessment(results))

			st.subheader(f"Productsysteem: {item}, 1 gebruikseenheid")
			st.session_state.results_database = st.data_editor(
				results,
				use_container_width=True,
				hide_index=True
			)
