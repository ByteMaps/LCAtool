from supabase import create_client
from dotenv import load_dotenv
import streamlit as st
import os
from pandas import json_normalize, to_numeric

TABLE = "test"

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
	return url, key, client, json_normalize(table.data)


def	save_row(newrow, client):
	client.table(TABLE).insert(newrow).execute()


def overwrite_db(data, client):
	'''Overwrite the database with the provided data. Make sure to use this with caution as it will delete all existing data and max batch size is 1000.
	Args:
		- data: a list of dictionaries containing the data to be saved
		- client_db: the Supabase client object
	Returns:
		None
	'''
	client.table(TABLE).delete().not_.is_("id", "null").execute()
	client.table(TABLE).insert(data).execute()


_, _, st.session_state.client, st.session_state.database = load_database()

st.title(TABLE)
# Extract the data from the APIResponse object
if not st.session_state.database.empty:
	float_cols = st.session_state.database.select_dtypes(include=['float']).columns
	new_data = st.data_editor(
		st.session_state.database,
		num_rows="dynamic",
		use_container_width=True,
		column_config={c: st.column_config.NumberColumn(step=0.00001) for c in float_cols},
		hide_index=True
	)

	if st.button("Opslaan"):
		try:
			new_data[float_cols] = new_data[float_cols].apply(to_numeric, errors='coerce')
			overwrite_db(new_data.to_dict(orient="records"), st.session_state.client)
			st.success("Data overgeschreven!")
		except Exception as e:
			st.error(f"Gefaald: {e}")