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

# Function to create a stacked bar chart
def create_stacked_bar_chart(df):
    fig = px.bar(df, x='Category', y='Value', color='Subcategory', 
                 title='Dynamic Stacked Bar Chart', barmode='stack')
    return fig


# Calculate percentage values within each Category
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

st.slider('Times of re-use', 0, 100, 10, 1)