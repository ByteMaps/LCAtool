import streamlit as st
import pandas as pd
import plotly.express as px
import random
from src.utils import FILE_PATH, load_all

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


def	calculate_impacts(amount=1, usage=10, itemtypes=[], flowtypes=[]):
	'''Calculate the impacts based on the current database'''
	if usage == 0: usage = 1
	results_db = st.session_state.database.copy()
	# Remove all columns containing 'units' in their header
	results_db = results_db.loc[:, ~results_db.columns.str.contains('units', case=False)]
	if itemtypes:
		filtered_db = results_db[results_db["itemtype"].isin(itemtypes)].copy()
	else: filtered_db = results_db
	if flowtypes:
		filtered_db = filtered_db[results_db["flowtype"].isin(flowtypes)].copy()
	filtered_db.loc[:, "quantity"] = filtered_db["quantity"] * amount							# Quantity
	filtered_db.loc[:, "quantity"] = filtered_db["quantity"].apply(lambda x: x*usage)			# Re-use
	filtered_db.iloc[:, 5:36] = filtered_db.iloc[:, 5:36].multiply(filtered_db["quantity"], axis=0)
	st.session_state.results_database = filtered_db


# Calculate percentage values within each Category
def	impact_assessment():

	figure_df = st.session_state.results_database.iloc[:,5:36].sum() # TODO rewrite using the flowtype as group


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

with st.form("IAform"):				# TODO add reset button
	col1, col2 = st.columns(2)
	with col1:
		re_use = st.slider('Keren hergebruik', 0, 100, 10, 1)
		quantity_multiplier = st.slider('Aantal gebruikseenheden', 1, 100, 1, 1)
	with col2:
		itemtypes = st.multiselect('Item types', options = st.session_state.database["itemtype"].unique())
		flowtypes = st.multiselect('Flow types', options = st.session_state.database["flowtype"].unique())
	submitted = st.form_submit_button("Maak")
	if submitted:
		calculate_impacts(quantity_multiplier, re_use, itemtypes, flowtypes)
		impact_assessment()

st.subheader("Productsysteem 1 gebruikseenheid")
st.session_state.results_database = st.data_editor(
	st.session_state.results_database,
	use_container_width=True,
	hide_index=True
)