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

def calc_timeline(item:str, re_use_impact:float, replacement_impact:float, re_use_times:int, replacement_time:int, time:int=365):
	'''Calculate the item's GWP impact over time based on usage & renewal'''
	timeline_impact = {}
	daily_usage = (float(re_use_times) / replacement_time) * re_use_impact

	for i in range(time):
		day = daily_usage + timeline_impact[i-1] if i > 0 else daily_usage
		if i % replacement_time == 0:
			day += replacement_impact
		timeline_impact[i] = round(day, 4)

	return (item, timeline_impact)

# if __name__=='__main__':
# 	impacts = pd.DataFrame(calc_timeline("Test Material", 0.03, 0.5, 5, 20)[1].items(), columns=["Days", "GWP impact"])
# 	print(impacts)

# 	fig = px.line(impacts, x="Days", y="GWP impact", title="GWP output item X over 1 year")
# 	fig.show(renderer="notebook")

def	format_results(item_dfs:dict, days:int=365):
	'''Get the item dataframe and extract GWP for usage and production categories for the item'''
	item_impacts = []
	for name, contents in item_dfs.items():
		df = contents[0]

		re_use_impact = df.query("flowtype == 'Usage'")['climate change'].sum() if 'Usage' in df['flowtype'].values else 0
		replacement_impact = df.query("flowtype != 'Usage'")['climate change'].sum()
		re_use_times = contents[2]
		replacement_time = contents[1]
		
		item = (name, re_use_impact, replacement_impact, re_use_times, replacement_time, days)
		item_impacts.append(item)

	return item_impacts

def	build_item_timeline(items:list[tuple]):
	timeline_dfs = []
	for item in items:
		timeline = calc_timeline(item[0], item[1], item[2], item[3], item[4], item[5])
		timeline_df = pd.DataFrame(list(timeline[1].items()), columns=["Days", f"GWP impact {item[0]}"])
		timeline_dfs.append(timeline_df.set_index("Days"))
	if timeline_dfs:
		impacts = pd.concat(timeline_dfs, axis=1).reset_index()
	else:
		impacts = pd.DataFrame()
	return impacts 													# type: ignore

def display_timeline_graph(impacts:pd.DataFrame, days:int=365):
	itemnames = [col for col in impacts.columns if col.startswith("GWP impact")]

	fig = px.line(impacts, x="Days", y=itemnames, title=f"GWP impact in {days} dagen")	# TODO instead of days, use key len from impacts
	# fig.show(renderer="browser")
	return fig

def	get_timeline(results, days):
	item_impacts = format_results(results, days)
	impacts = build_item_timeline(item_impacts)
	return display_timeline_graph(impacts, days)