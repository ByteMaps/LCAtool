"""This file is for loading and saving the JSON objects to the appropriate files"""

import pandas as pd
import streamlit as st
from re import sub
from uuid import uuid4
from supabase import create_client
from dotenv import load_dotenv
import os
from pandas import json_normalize, to_numeric

TABLE = "main"

FLOWS = ['Production','Transport','Packaging','Usage','End of Life']
TYPES = ['None']


def	add_to_db(name, itemtype, flowtype, description, df, entrytype=False):
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
	df["Impact category"] = [sub(r'\s', ' ', x.lower()) for x in df["Impact category"]]

	# Set up row
	row_data = {
		"id": str(uuid4()),
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

	save_newrow(row_data)


def	calculate_impacts(df:pd.DataFrame, item:str, amount=1, usage=10, flowtypes:list[str]=[]):
	'''
	Calculate the impacts based on the current database
		- item: the item to calculate impacts for
		- amount: the number of usage units
		- usage: the number of times the item is reused
		- flowtypes: the types of flows to include in the calculation, if empty, all flows are included

	Returns a filtered dataframe with the impacts for the specified item.
	'''

	# Ensure usage is at least 1 to avoid division by zero or no impact calculation
	if usage == 0: usage = 1

	# Work on a copy to avoid modifying the original dataframe
	results_db = df.copy()

	# Remove all columns containing 'units' and standardize column names by removing ' amount'
	results_db = results_db.loc[:, ~results_db.columns.str.contains('units', case=False)]
	results_db.columns = results_db.columns.str.replace(' amount', '', regex=False)

	# Filter the dataframe for the specified item
	filtered_db = results_db[results_db["itemtype"] == item].copy()

	# If flowtypes are specified, filter further by those flowtypes
	if flowtypes:
		filtered_db = filtered_db[results_db["flowtype"].isin(flowtypes)].copy()

	# Adjust the 'quantity' column for the total amount and for usage-based flows
	filtered_db.loc[:, "quantity"] = filtered_db["quantity"] * amount
	filtered_db.loc[filtered_db["flowtype"] == "Usage", "quantity"] = filtered_db.loc[filtered_db["flowtype"] == "Usage", "quantity"].apply(lambda x: x * usage)

	# Multiply all numeric impact columns (excluding metadata and unit columns) by the adjusted quantity
	cols_to_multiply = [col for col in filtered_db.columns if col not in filtered_db.columns[:5] and not col.endswith("units")]
	filtered_db[cols_to_multiply] = filtered_db[cols_to_multiply].apply(pd.to_numeric, errors='coerce')
	filtered_db[cols_to_multiply] = filtered_db[cols_to_multiply].apply(lambda x: x * filtered_db["quantity"])

	return filtered_db

#=====================================================================================================================================================================

def	load_database():
	'''Build the supabase client and return the url, key and client for use in the app.
	Returns:
		url: the URL of the Supabase instance
		key: the API key for the Supabase instance
		client_db: the Supabase client object
	'''
	load_dotenv()

	url = os.getenv("SUPABASE_URL")
	key = os.getenv("SUPABASE_KEY")
	client = create_client(url, key) # type: ignore
	table = client.table(TABLE).select('*').execute()
	database = json_normalize(table.data)
	return client, database


def	save_newrow(newrow):
	if "client" not in st.session_state:
		st.session_state.client, st.session_state.database = load_database()

	st.session_state.client.table(TABLE).insert(newrow).execute()


def overwrite_db(data, client):
	'''Overwrite the database with the provided data. Make sure to use this with caution as it will delete all existing data and max batch size is 1000.
	Args:
		- data: a list of dictionaries containing the data to be saved
		- client_db: the Supabase client object
	Returns:
		None
	'''
	if len(data) > 1000:
		raise ValueError(f"Batch size {len(data)} exceeds maximum of 1000 records")

	# Fetch existing data as backup
	backup = client.table(TABLE).select('*').execute()

	try:
			client.table(TABLE).delete().not_.is_("id", "null").execute()
			client.table(TABLE).insert(data).execute()
	except Exception as e:
		# Attempt to restore backup if available
		if backup and backup.data:
			client.table(TABLE).insert(backup.data).execute()
		raise Exception(f"Failed to overwrite database: {str(e)}")
	client.table(TABLE).delete().not_.is_("id", "null").execute()
	client.table(TABLE).insert(data).execute()


# Remove trailing _1, _2, etc. from impact category names
def clean_category(cat):
	return sub(r'_\d$', '', cat)