from supabase import create_client
from dotenv import load_dotenv
from pandas import json_normalize
import os

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
	client_db = create_client(url, key) # type: ignore
	return url, key, client_db


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


if __name__=='__main__':
	url, key, client = load_database()
	# print(client.table(TABLE).select('*').execute().data[0])
	save_row({'name': 'EOL', 'description': None, 'quantity': 0.134, 'itemtype': 'Single Use', 'flowtype': 'End of Life', 'acidification amount': -0.0152, 'acidification units': 'molc H+ eq', 'climate change amount': 1.09103, 'climate change units': 'kg CO2 eq', 'freshwater ecotoxicity amount': -0.07056, 'freshwater ecotoxicity units': 'CTUe', 'freshwater eutrophication amount': -3.7e-06, 'freshwater eutrophication units': 'kg P eq', 'human toxicity, cancer effects amount': -1.26e-09, 'human toxicity_1, cancer effects units': 'CTUh', 'human toxicity_2, non-cancer effects amount': -5.54e-08, 'human toxicity_3, non-cancer effects units': 'CTUh', 'ionizing radiation e (interim) amount': -2.5e-06, 'ionizing radiation e (interim) units': 'CTUe', 'ionizing radiation hh amount': -0.25371, 'ionizing radiation hh units': 'kBq U235 eq', 'land use amount': '0', 'land use units': 'kg C deficit', 'marine eutrophication amount': -0.00154, 'marine eutrophication units': 'kg N eq', 'mineral, fossil & ren resource depletion amount': -1.96e-07, 'mineral_1, fossil & ren resource depletion units': 'kg Sb eq', 'ozone depletion amount': -2.09e-07, 'ozone depletion units': 'kg CFC-11 eq', 'particulate matter amount': -0.00084, 'particulate matter units': 'kg PM2.5 eq', 'photochemical ozone formation amount': -0.00492, 'photochemical ozone formation units': 'kg NMVOC eq', 'terrestrial eutrophication amount': -0.01591, 'terrestrial eutrophication units': 'molc N eq', 'water resource depletion amount': 0.0005, 'water resource depletion units': 'm3 water eq', 'id': '03817249-a62c-459b-82f3-e9cf4b12d9bd'}, client)
