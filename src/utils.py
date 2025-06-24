import json

class Material:
	def __init__(self, name):
		self.name = name
		self.quantity = 0
		self.impact_categories = []
		self.impact_values = {}
		self.reference_units = {}

	def add_impact_category(self, category, value, ref_unit):
		self.impact_categories.append(category)
		self.impact_values[category] = value
		self.reference_units[category] = ref_unit

class Transport:
	def __init__(self, name):
		self.name = name
		self.quantity = 0
		self.impact_categories = []
		self.impact_values = {}
		self.reference_units = {}

	def add_impact_category(self, category, value, ref_unit):
		self.impact_categories.append(category)
		self.impact_values[category] = value
		self.reference_units[category] = ref_unit

def load_items_from_json(file_path, obj_type):
	with open(file_path, 'r') as file:
		data = json.load(file)
		items = []
		for name, impacts in data.items():
			item = Material(name) if obj_type=="material" else Transport(name)
			for impact in impacts:
				item.add_impact_category(
					impact["Impact category"],
					impact["Result"],
					impact["Reference unit"]
				)
			items.append(item)
	return items

if __name__ == "__main__":
	file_path = 'src/synth_transport_data.json'
	materials = load_items_from_json(file_path, "transport")
	for material in materials:
		print(f"Material: {material.name}")
		for category in material.impact_categories:
			print(f"  {category}: {material.impact_values[category]} ({material.reference_units[category]})")