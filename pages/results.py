import streamlit as st
import pandas as pd
import plotly.express as px
import random

impact_categories = ['GWP', 'Ozone Depletion', 'Photochem. Ozone Form.', 'Acidification', 'Eutrophication',
					'Human Toxicity', 'FMT Ecotoxicity', 'Ionising Radiation', 'Particulate Matter', 'Land Use',
					'Resource Depletion', 'Water Depletion']

standard = ['Usage', 'Transport', 'End of Life', 'Production', 'Packaging']

# Sample dynamic data generator
def generate_data(flows):
	data = []
	for category in impact_categories:
		# Choose a random number of flows for each category
		n_flows = random.randint(1, len(flows))
		selected_flows = random.sample(flows, n_flows)
		for flow in selected_flows:
			value = random.randint(5, 100)
			data.append({'Impact Category': category, 'Flows': flow, 'Value': value})
	return pd.DataFrame(data)

def	calculate_impacts(N, itemtypes, flowtypes):
	'''Calculate the impacts based on the current database'''

	results_db = st.session_state.database.copy()
	if itemtypes:
		filtered_db = results_db[results_db["itemtype"].isin(itemtypes)].copy()
	else: filtered_db = results_db
	if flowtypes:
		filtered_db = filtered_db[results_db["flowtype"].isin(flowtypes)].copy()
	filtered_db.loc[:, "quantity"] = filtered_db["quantity"] * N
	st.session_state.results_database = filtered_db


# Calculate percentage values within each Category
def	impact_assessment(df):
	if 'flows' not in st.session_state:
		data = generate_data(standard)
	else:
		data = generate_data(st.session_state.flows)
	data_percent = data.copy()
	data_percent['Percent'] = data_percent.groupby('Impact Category')['Value'].transform(lambda x: x / x.sum() * 100)
	fig = px.bar(
		data_percent,
		x='Impact Category',
		y='Percent',
		color='Flows',
		title='Impact Category Assessment',
		barmode='stack',
		labels={'Percent': 'Percentage (%)'}
	)
	st.plotly_chart(fig)

with st.form("IAform"):
	col1, col2 = st.columns(2)
	with col1:
		re_use = st.slider('Keren hergebruik', 0, 100, 10, 1)
		quantity_multiplier = st.slider('Aantal', 1, 100, 1, 1)
	with col2:
		itemtypes = st.multiselect('Item types', options = st.session_state.database["itemtype"].unique())
		flowtypes = st.multiselect('Flow types', options = st.session_state.database["flowtype"].unique())
	submitted = st.form_submit_button("Maak")
	if submitted:
		calculate_impacts(quantity_multiplier, itemtypes, flowtypes)
		# impact_assessment(st.session_state.results_database)

st.session_state.results_database = st.data_editor(
	st.session_state.results_database,
	use_container_width=True,
	hide_index=True
)