import streamlit as st
from src.utils import *
from src.visualisations import *

# SESSION ========================================================================================================================================

if 'database' not in st.session_state:	# TODO change loaded
	st.session_state.database = load_all()

if 'submissions' not in st.session_state:
	st.session_state.submissions = {}

def	reset():
	'''Clear the submissions to enter new comparisons'''
	st.session_state.submissions.clear()

# SESSION ========================================================================================================================================

col1, col2 = st.columns(2)

with col1:
	st.session_state.comparison = st.multiselect('Items om te vergelijken', options = st.session_state.database["itemtype"].unique()) # TODO change if needed
with col2:
	st.button("Reset vergelijking", on_click=reset)


for item in st.session_state.comparison:
	with st.form(f"{item}"):
		st.subheader(f"{item}")
		col1, col2 = st.columns(2)
		with col1:
			re_use = st.slider('Keren hergebruik', 0, 100, 10, 1)
			quantity_multiplier = st.slider('Aantal gebruikseenheden', 1, 100, 1, 1)
		with col2:
			flowtypes = st.multiselect('Flow types', options = st.session_state.database["flowtype"].unique())
			rep_time = st.text_input('Tijd tot vervanging (dagen)', placeholder='100')


		submitted = st.form_submit_button("Maak")
		if submitted:
			results = calculate_impacts(st.session_state.database.copy(), item, quantity_multiplier, re_use, flowtypes)

			st.session_state.submissions[item] = results

			st.subheader(f"Productsysteem: {item}, 1 gebruikseenheid")
			st.data_editor(
				results,
				use_container_width=True,
				hide_index=True
			)

if len(st.session_state.submissions.keys()) == len(st.session_state.comparison) and st.session_state.comparison:
	st.divider()
	st.subheader("Stacked barcharts per result")
	for sub_key, sub_values in st.session_state.submissions.items():
		st.plotly_chart(impact_assessment(sub_key, sub_values))

	if len(st.session_state.submissions.keys()) >= 2:
		st.divider()
		st.subheader("Clustered stacked barchart")
		names = [keys for keys, _ in st.session_state.submissions.items()]
		results = [dfs for _, dfs in st.session_state.submissions.items()]

		st.plotly_chart(impact_comparison(names, results))

	