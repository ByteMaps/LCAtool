import streamlit as st
import pandas as pd

MATERIAL_PATH = "src/materials.csv"

st.set_page_config(layout="wide")
st.title("Materials Dataframe")

# Initialize session state
if 'materials' not in st.session_state:
	st.session_state.materials = pd.DataFrame()

# File path input
file_path = st.text_input("File Path:", value=MATERIAL_PATH)

# Load and Save buttons
col1, col2 = st.columns(2)

with col1:
	if st.button("Load CSV"):
		try:
			st.session_state.materials = pd.read_csv(file_path, sep=";")
			st.success("File loaded successfully!")
		except Exception as e:
			st.error(f"Error loading file: {e}")

with col2:
	if st.button("Save CSV"):
		try:
			st.session_state.materials.to_csv(file_path, index=False, sep=";")
			st.success("File saved successfully!")
		except Exception as e:
			st.error(f"Error saving file: {e}")

# Data editor
if not st.session_state.materials.empty:
	st.session_state.materials = st.data_editor(
		st.session_state.materials,
		num_rows="dynamic",
		use_container_width=True
	)
else:
	st.info("Load a CSV file to start editing")