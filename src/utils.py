"""This file is for loading and saving the JSON objects to the appropriate files"""

import json
import os
import pandas as pd
import streamlit as st

FILE_PATH = "src/"

MATERIALS = f'{FILE_PATH}materials.csv'
TRANSPORT = f'{FILE_PATH}transport.csv'
PROCESSES = f'{FILE_PATH}processes.csv'

FLOWS = ['Production','Transport','Packaging','Usage','End of Life']

# DB ========================================================================================================================================

def load_materials():
	st.session_state.materials = pd.DataFrame()
	st.session_state.materials = pd.read_csv(MATERIALS, sep=";")

def load_transport():
	st.session_state.transport = pd.DataFrame()
	st.session_state.transport = pd.read_csv(TRANSPORT, sep=";")

def load_processes():
	st.session_state.processes = pd.DataFrame()
	st.session_state.processes = pd.read_csv(PROCESSES, sep=";")

def	load_all():
	load_materials()
	load_processes()
	load_transport()

# FUNCTIONS ========================================================================================================================================

def	add_to_db(name, itemtype, flowtype, description, df):
	'''Format the new dataset and prepare to add to one of the databases'''

	# Prepare data
	df["Impact category"] = [x.lower() for x in df["Impact category"]]

	results_dict = pd.Series(df["Result"].values, index=df["Impact category"]).to_dict()
	units_dict = pd.Series(df["Reference unit"].values, index=df["Impact category"]).to_dict()
	impact_tuples = {k: (results_dict[k], units_dict[k]) for k in results_dict}

	# Set up row
	row_data = {
		"name": name,
		"description": description,
		"quantity": 1,
		"flowtype": flowtype
	}

	# Add the impact values
	for k, (value, unit) in impact_tuples.items():
		row_data[f"{k} amount"] = value
		row_data[f"{k} units"] = unit

	save_newrow(row_data, itemtype)


def save_newrow(row_data, itemtype):
	'''Save the new item based on type, then reload appropriate db'''
	if itemtype == 'Materiaal':
		if 'materials' not in st.session_state:
			load_materials()
		materials = st.session_state.materials
		materials.loc[len(materials)] = row_data
		st.session_state.materials.to_csv(MATERIALS, index=False, sep=";")
		load_materials()

	if itemtype == 'Proces':
		if 'processes' not in st.session_state:
			load_processes()
		processes = st.session_state.processes
		processes.loc[len(processes)] = row_data
		st.session_state.processes.to_csv(PROCESSES, index=False, sep=";")
		load_processes()

	if itemtype == 'Transport':
		if 'transport' not in st.session_state:
			load_transport()
		transport = st.session_state.transport
		transport.loc[len(transport)] = row_data
		st.session_state.transport.to_csv(TRANSPORT, index=False, sep=";")
		load_transport()