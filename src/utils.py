import json
import os

FILE_PATH = "src/synth_transport_data.json"

# Load JSON from file
def load_json(path=FILE_PATH):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

# Save JSON to file
def save_json(data, path=FILE_PATH):
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