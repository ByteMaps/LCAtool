"""This file is for loading and saving the JSON objects to the appropriate files"""

import json
import os
import pandas as pd

FILE_PATH = "src/synth_transport_data.json"


def load_json(path=FILE_PATH):
    '''Load the data object from a file given path'''
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_json(data, path=FILE_PATH):
    '''Save the data object to a file given data and path, overwriting the whole file'''
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
        

def	format_csv():
	df = pd.read_excel("src/materials.xlsx")

	# If you have multiple materials in the Excel, group them:
	materials = df.groupby("Material name")

	# Prepare columns for impact categories
	impact_categories = df["Impact category"].unique()
	# Ensure consistent ordering
	impact_categories.sort()

	# Build header
	header = ["material name", "quantity"]
	for category in impact_categories:
		header.append(f"{category} amount")
		header.append(f"{category} units")

	# Prepare rows
	rows = []

	for material_name, group in materials:
		row = [material_name, 1]  # quantity is set to 1
		# Create a mapping: impact category -> (amount, unit)
		impact_map = {
			r["Impact category"]: (r["Result"], r["Reference unit"])
			for _, r in group.iterrows()
		}
		for category in impact_categories:
			amount, unit = impact_map.get(category, ("", ""))
			row.append(amount)
			row.append(unit)
		rows.append(row)

	# Convert to DataFrame
	output_df = pd.DataFrame(rows, columns=header)

	# Save to CSV
	output_df.to_csv("output.csv", index=False, sep=";")
        
def test_json():
	file_path = 'src/synth_transport_data.json'
	transports = load_json()
	for category in transports['TransportType_1']:
		print(f"Cat: {category["Impact category"]} at {category["Result"]} {str(category["Reference unit"])}")
	print(f"{len(transports['TransportType_1'])} categories indexed")

	transports['Truck'] = transports.pop('TransportType_1')
	print(transports)
	save_json(transports)

if __name__ == "__main__":
     format_csv()