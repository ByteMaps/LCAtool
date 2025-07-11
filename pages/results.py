import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import load_all

if 'database' not in st.session_state:
	st.session_state.database = load_all()

def	calculate_impacts(df, item, amount=1, usage=10, flowtypes=[]):
	'''Calculate the impacts based on the current database'''
	if usage == 0: usage = 1
	results_db = df #st.session_state.database.copy()
	# Remove all columns containing 'units' in their header
	results_db = results_db.loc[:, ~results_db.columns.str.contains('units', case=False)]
	results_db.columns = results_db.columns.str.replace(' amount', '', regex=False)
	filtered_db = results_db[results_db["itemtype"] == item].copy()
	if flowtypes:
		filtered_db = filtered_db[results_db["flowtype"].isin(flowtypes)].copy()
	filtered_db.loc[:, "quantity"] = filtered_db["quantity"] * amount							# Quantity
	filtered_db.loc[filtered_db["flowtype"] == "Usage", "quantity"] = filtered_db.loc[filtered_db["flowtype"] == "Usage", "quantity"].apply(lambda x: x * usage)  # Re-use only for 'Usage' flowtype
	filtered_db.iloc[:, 5:36] = filtered_db.iloc[:, 5:36].multiply(filtered_db["quantity"], axis=0)
	return filtered_db


# Calculate percentage values within each Category
def	impact_assessment(df):
	'''Create a stacked barchart with the results'''

	figure_df = df.drop(['name', 'description', 'quantity', 'itemtype'], axis=1)
	figure_df = figure_df.melt(id_vars=['flowtype'], var_name="Impact Category", value_name="Value")
	figure_df = figure_df.groupby(["Impact Category", "flowtype"], as_index=False)["Value"].sum()
	figure_df = figure_df.rename(columns={'flowtype':'Flows'})

	data_percent = figure_df.copy()
	data_percent['Percent'] = figure_df.groupby('Impact Category')['Value'].transform(lambda x: x / x.sum() * 100)
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
			impact_assessment(results)

			st.subheader(f"Productsysteem: {item}, 1 gebruikseenheid")
			st.session_state.results_database = st.data_editor(
				results,
				use_container_width=True,
				hide_index=True
			)
