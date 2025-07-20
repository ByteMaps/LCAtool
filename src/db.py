from supabase import create_client, Client
from dotenv import load_dotenv
from pandas import json_normalize
import os

def	load_database():
	load_dotenv()

	url = os.getenv("SUPABASE_URL")
	key = os.getenv("SUPABASE_KEY")
	supabase = create_client(url, key) # type: ignore
	return url, key, supabase


def	get_data(database):
	response = database.table('LCAdatabase').select('*').execute()
	data = json_normalize(response.data)
	return data


def	save_row(newrow, database):
	database.table('LCAdatabase').insert(newrow).execute()


def save_database():
	pass


if __name__=='__main__':
	url, key, database = load_database()
	get_data(database)