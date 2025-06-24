import streamlit as st
from src.utils import *

st.title("LCA Tool voor verzorgend wassen")
if "form1_submitted" not in st.session_state:
	st.session_state.form1_submitted = False
if "form2_submitted" not in st.session_state:
	st.session_state.form2_submitted = False

st.session_state.material_objs = load_items_from_json("src/synth_material_data.json", "materials")
st.session_state.transport_objs = load_items_from_json("src/synth_transport_data.json", "transport")

if not st.session_state.form1_submitted:
	with st.form("my_form"):
		st.write("Choose the materials and transport types:")

		# Multi-select dropdown
		selected_materials = st.multiselect(
			"Materials",
			options=[item.name for item in st.session_state.material_objs],
		)
		selected_transport = st.multiselect(
			"Transport Options",
			options=[item.name for item in st.session_state.transport_objs],
		)

		# Submit button
		submitted = st.form_submit_button("Submit")
		if submitted:
			st.session_state.materials = selected_materials
			st.session_state.transport = selected_transport
			st.session_state.form1_submitted = True

if st.session_state.form1_submitted and not st.session_state.form2_submitted:
	st.write(f"Please enter the quantities for materials and transport")

	with st.form("quantities_form"):
		material_quantities = {}
		transport_quantities = {}

		for material in st.session_state.materials:
			name = material
			value = st.number_input(f"{name}", min_value=0.0, step=0.1, key=f"quant_mat_{material}")
			material_quantities[name] = value

		st.write("Transport Options")

		for transport in st.session_state.transport:
			name = transport
			value = st.number_input(f"Type {name}", min_value=0.0, step=0.1, key=f"quant_trans_{transport}")
			transport_quantities[name] = value

		submit_values = st.form_submit_button("Enter")
		if submit_values:
			st.session_state.form2_submitted = True
			st.session_state.material_quantity = material_quantities
			st.session_state.transport_quantity = transport_quantities

if st.session_state.form1_submitted and st.session_state.form2_submitted:
	st.write("Please navigate to graphs for the results, see the sidebar.")
