import streamlit as st
import json
import os
import src.utils as utils

MAT_PATH = "src/synth_material_data.json"

# App title
st.title("Material Editor")

st.session_state.data = utils.load_json(MAT_PATH)

# Choose material
material_options = list(st.session_state.data.keys())
selected_mode = st.selectbox("Select material", material_options)

# Extract editable data
impact_data = st.session_state.data[selected_mode]
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
	st.session_state.data[selected_mode] = edited_df
	st.success("Changes stored in memory.")

	col1, col2 = st.columns(2)
	with col1:
		if st.button("Overwrite default file"):
			utils.save_json(st.session_state.data, MAT_PATH)
			st.success(f"Saved to `{MAT_PATH}`")

	with col2:
		json_str = json.dumps(st.session_state.data, indent=4)
		st.download_button(
			label="Download updated JSON",
			data=json_str,
			file_name="modified_data.json",
			mime="application/json"
		)
