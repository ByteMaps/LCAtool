import streamlit as st
import pandas as pd
import plotly.express as px
import random

impact_categories = ['GWP', 'Ozone Depletion', 'Photochem. Ozone Form.', 'Acidification', 'Eutrophication',
					'Human Toxicity', 'FMT Ecotoxicity', 'Ionising Radiation', 'Particulate Matter', 'Land Use',
					'Resource Depletion', 'Water Depletion']

flows = ['Usage', 'Transport', 'End of Life', 'Production', 'Packaging']

# Sample dynamic data generator
def generate_data():
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


# Generate or upload your data
# uploaded_file = st.file_uploader("Upload your data", type="csv")
# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     x_col = st.selectbox("Select X column", df.columns)
#     y_col = st.selectbox("Select Y column", df.columns)
#     color_col = st.selectbox("Select color/stack column", df.columns)
#     fig = px.bar(df, x=x_col, y=y_col, color=color_col, barmode='stack')
#     st.plotly_chart(fig)
# else:
data = generate_data()

# Calculate percentage values within each Category
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