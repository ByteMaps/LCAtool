import json
import os


"""This file is for loading and saving the JSON objects to the appropriate files"""

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
        

if __name__ == "__main__":
	file_path = 'src/synth_transport_data.json'
	transports = load_json()
	for category in transports['TransportType_1']:
		print(f"Cat: {category["Impact category"]} at {category["Result"]} {str(category["Reference unit"])}")
	print(f"{len(transports['TransportType_1'])} categories indexed")

	transports['Truck'] = transports.pop('TransportType_1')
	print(transports)
	save_json(transports)