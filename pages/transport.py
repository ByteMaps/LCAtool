import streamlit as st
import json
import os

DEFAULT_FILE_PATH = "src/synth_transport_data.json"

# Load JSON from file or upload
def load_json(file):
    try:
        return json.load(file)
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
        return {}

# Save JSON to disk
def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# App title
st.title("Transport Editor")

if os.path.exists(DEFAULT_FILE_PATH):
	with open(DEFAULT_FILE_PATH, "r") as f:
		data = json.load(f)
else:
	st.error(f"Default file `{DEFAULT_FILE_PATH}` not found.")
	st.stop()

# Choose material
material_options = list(data.keys())
selected_mode = st.selectbox("Select transport", material_options)

# Extract editable data
impact_data = data[selected_mode]
st.subheader(f"Editing: {selected_mode}")

# Show editable grid
edited_df = st.data_editor(
    impact_data,
    num_rows="dynamic",  # or 'dynamic' if you want to let users add/remove rows
    column_config={
        "Impact category": st.column_config.TextColumn(disabled=False),
        "Reference unit": st.column_config.TextColumn(disabled=True),
        "Result": st.column_config.NumberColumn(format="%.10f"),
    },
    use_container_width=True
)

# Update and save/download
if st.button("Save Changes"):
	data[selected_mode] = edited_df
	st.success("Changes stored in memory.")

	col1, col2 = st.columns(2)
	with col1:
		if st.button("Overwrite default file"):
			save_json(data, DEFAULT_FILE_PATH)
			st.success(f"Saved to `{DEFAULT_FILE_PATH}`")

	with col2:
		json_str = json.dumps(data, indent=4)
		st.download_button(
			label="Download updated JSON",
			data=json_str,
			file_name="modified_data.json",
			mime="application/json"
		)