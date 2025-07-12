"""This file is for loading and saving the JSON objects to the appropriate files"""

import pandas as pd
import streamlit as st
from re import sub
import plotly.express as px

FILE_PATH = "src/database.csv"

FLOWS = ['Production','Transport','Packaging','Usage','End of Life']
TYPES = ['None']


def	load_all(filepath=FILE_PATH):
	'''
	Load database from file
		- filepath: the path to the database file
	'''
	database = pd.DataFrame()
	database = pd.read_csv(filepath, sep=";", index_col=False)
	return database


def	add_to_db(name, itemtype, flowtype, description, df, entrytype=False, database=load_all()):
	'''
	Format the new dataset and prepare to add to one of the databases.
		- name: the name of the item
		- itemtype: the type of the item
		- flowtype: the type of the flow
		- description: the description of the item
		- df: the dataframe with the impact values
		- entrytype: whether the input is from Excel or OpenLCA
	'''

	# Clean data
	df["Impact category"] = [sub(r'\s+', ' ', x.lower()) for x in df["Impact category"]]

	# Set up row
	row_data = {
		"name": name,
		"description": description,
		"quantity": 1,
		"itemtype": itemtype,
		"flowtype": flowtype
	}

	if entrytype:
		# Input from Excel
		results_dict = pd.Series(df["Result"].values, index=df["Impact category"]).to_dict()
		units_dict = pd.Series(df["Reference unit"].values, index=df["Impact category"]).to_dict()
	else:
		# Input from OpenLCA directly
		results_dict = pd.Series(df["Result"].apply(lambda x: float(x.split(' ')[0])).values, index=df["Impact category"]).to_dict()
		units_dict = pd.Series(df["Result"].apply(lambda x: ' '.join(x.split(' ')[1:])).values, index=df["Impact category"]).to_dict()

	# Add the impact values
	impact_tuples = {k: (results_dict[k], units_dict[k]) for k in results_dict}
	for k, (value, unit) in impact_tuples.items():
		row_data[f"{k} amount"] = float(value)
		row_data[f"{k} units"] = unit

	save_newrow(row_data, database)


def save_newrow(row_data, database=load_all()):
	'''
	Save the new item based on type, then reload appropriate database
		- row_data: the data to save, as a dictionary with keys matching the database columns

	Returns the updated database.
	'''
	database.loc[len(database)] = row_data
	st.session_state.database.to_csv(FILE_PATH, index=False, sep=";")
	st.session_state.database = load_all()


def	calculate_impacts(df, item, amount=1, usage=10, flowtypes=[]):
	'''
	Calculate the impacts based on the current database
		- item: the item to calculate impacts for
		- amount: the number of usage units
		- usage: the number of times the item is reused
		- flowtypes: the types of flows to include in the calculation, if empty, all flows are included

	Returns a filtered dataframe with the impacts for the specified item.
	'''

	if usage == 0: usage = 1
	results_db = df.copy()
	results_db = results_db.loc[:, ~results_db.columns.str.contains('units', case=False)]
	results_db.columns = results_db.columns.str.replace(' amount', '', regex=False)
	filtered_db = results_db[results_db["itemtype"] == item].copy()
	if flowtypes:
		filtered_db = filtered_db[results_db["flowtype"].isin(flowtypes)].copy()
	filtered_db.loc[:, "quantity"] = filtered_db["quantity"] * amount							# Quantity
	filtered_db.loc[filtered_db["flowtype"] == "Usage", "quantity"] = filtered_db.loc[filtered_db["flowtype"] == "Usage", "quantity"].apply(lambda x: x * usage)  # Re-use only for 'Usage' flowtype
	filtered_db.iloc[:, 5:36] = filtered_db.iloc[:, 5:36].multiply(filtered_db["quantity"], axis=0)

	return filtered_db


if __name__ == '__main__':
	st.session_state.database = load_all()