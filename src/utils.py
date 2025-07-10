"""This file is for loading and saving the JSON objects to the appropriate files"""

import pandas as pd
import streamlit as st
import numpy as np
from re import sub

FILE_PATH = "src/database.csv"

FLOWS = ['Production','Transport','Packaging','Usage','End of Life']
TYPES = ['None']

# DB ========================================================================================================================================

def	load_all(filepath=FILE_PATH):
	'''Load database from file'''
	database = pd.DataFrame()
	database = pd.read_csv(filepath, sep=";", index_col=False)
	return database


# FUNCTIONS ========================================================================================================================================

def	add_to_db(name, itemtype, flowtype, description, df):
	'''Format the new dataset and prepare to add to one of the databases'''

	# Prepare data
	df["Impact category"] = [sub(r'\s+', ' ', x.lower()) for x in df["Impact category"]]

	results_dict = pd.Series(df["Result"].values, index=df["Impact category"]).to_dict()
	units_dict = pd.Series(df["Reference unit"].values, index=df["Impact category"]).to_dict()
	impact_tuples = {k: (results_dict[k], units_dict[k]) for k in results_dict}

	# Set up row
	row_data = {
		"name": name,
		"description": description,
		"quantity": 1,
		"itemtype": itemtype,
		"flowtype": flowtype
	}

	# Add the impact values
	for k, (value, unit) in impact_tuples.items():
		row_data[f"{k} amount"] = float(value)
		row_data[f"{k} units"] = unit

	save_newrow(row_data)


def save_newrow(row_data):
	'''Save the new item based on type, then reload appropriate db'''
	if 'database' not in st.session_state:
		load_all()
	database = st.session_state.database
	database.loc[len(database)] = row_data
	st.session_state.database.to_csv(FILE_PATH, index=False, sep=";")
	st.session_state.database = load_all()

if __name__ == '__main__':
	st.session_state.database = load_all()
	print(st.session_state.database)