import pandas as pd
import plotly.express as px
from numpy import zeros

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

def calc_timeline(re_use_impact, renewal_impact, re_use_times, renewal_time, time=365):
	'''Calculate the item's GWP impact over time based on usage & renewal'''
	timeline_impact = dict()
	daily_usage = (re_use_times / renewal_time) * re_use_impact

	for i in range(time):
		day = daily_usage + timeline_impact[i-1] if i > 0 else daily_usage
		if i % renewal_time == 0:
			day += renewal_impact
		timeline_impact[i] = round(day, 4)

	return timeline_impact						# ? Normalise compared to other outputs?

if __name__=='__main__':
	impacts = pd.DataFrame(calc_timeline(0.03, 0.5, 5, 20).items(), columns=["Days", "GWP impact"])
	print(impacts)

	fig = px.line(impacts, x="Days", y="GWP impact", title="GWP output item X over 1 year")
	fig.show(renderer="notebook")