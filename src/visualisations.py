import pandas as pd
import plotly.express as px

def impact_assessment(name, df):
	"""
	Create a stacked barchart with the impact results, assessed per flow per impact category.
	- name: the name of the item
	- df: the dataframe with the impact results

	Returns a Plotly figure object.
	"""
	# Drop unnecessary columns and reshape data
	cols_to_drop = ['name', 'description', 'quantity', 'itemtype']
	figure_df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
	figure_df = figure_df.melt(id_vars=['flowtype'], var_name="Impact Category", value_name="Value")
	figure_df = figure_df.groupby(["Impact Category", "flowtype"], as_index=False)["Value"].sum()
	figure_df["Value"] = figure_df["Value"].clip(lower=0)
	figure_df = figure_df.rename(columns={'flowtype': 'Flows'})

	# Calculate percent per impact category
	figure_df['Percent'] = figure_df.groupby('Impact Category')['Value'].transform(lambda x: x / x.sum() * 100)

	fig = px.bar(
		figure_df,
		x='Impact Category',
		y='Percent',
		color='Flows',
		title=f'ICA {name}',
		barmode='stack',
		labels={'Percent': 'Percentage (%)'}
	)
	return fig


def impact_comparison(names, dfs):
	"""
	Create a clustered barchart comparing multiple items, showing percentual impact values per impact category.
	- names: list of item names corresponding to each dataframe
	- dfs: list of dataframes with impact results

	Returns a Plotly figure object.
	"""
	combined = []
	cols_to_drop = ['name', 'description', 'quantity', 'itemtype']
	for name, df in zip(names, dfs):
		temp_df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
		temp_df = temp_df.melt(id_vars=['flowtype'], var_name="Impact Category", value_name="Value")
		temp_df = temp_df.groupby("Impact Category", as_index=False)["Value"].sum()
		temp_df["Value"] = temp_df["Value"].clip(lower=0)
		temp_df["Name"] = name
		combined.append(temp_df)
	result_df = pd.concat(combined, ignore_index=True)

	# Calculate percent per impact category
	result_df['Percent'] = result_df.groupby('Impact Category')['Value'].transform(lambda x: x / x.sum() * 100)

	fig = px.bar(
		result_df,
		x="Impact Category",
		y="Percent",
		color="Name",
		barmode="group",
		title="Impact Comparison (Percentual)",
		labels={"Percent": "Percentual Impact (%)"}
	)
	return fig