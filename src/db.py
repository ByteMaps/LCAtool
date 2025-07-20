from supabase import create_client
from dotenv import load_dotenv
import streamlit as st
import os
from pandas import json_normalize

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
	return url, key, client, table


def	save_row(newrow, client_db):
	client_db.table(TABLE).insert(newrow).execute()


def overwrite_db(data, client_db):
	'''Overwrite the database with the provided data. Make sure to use this with caution as it will delete all existing data and max batch size is 1000.
	Args:
		- data: a list of dictionaries containing the data to be saved
		- client_db: the Supabase client object
	Returns:
		None
	'''
	client_db.table(TABLE).delete().not_.is_("id", "null").execute()
	client_db.table(TABLE).insert(data).execute()


_, _, client, table = load_database()

st.title(TABLE)
# Extract the data from the APIResponse object
table_data = table.data if hasattr(table, "data") else []
new_data = st.data_editor(
	json_normalize(table_data),
	num_rows="dynamic",
	use_container_width=True,
	hide_index=True
)