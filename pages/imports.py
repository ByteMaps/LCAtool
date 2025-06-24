import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload your data", type="csv")

# if st.session_state.material_quantity and st.session_state.transport_quantity \
# 	and st.session_state.material_objs and st.session_state.transport_objs:
# 	materials_df = pd.DataFrame({
# 		"Material": [obj.name for obj in st.session_state.material_objs],
# 		"Quantity": st.session_state.material_quantity
# 	})

# 	transports_df = pd.DataFrame({
# 		"Transport": [obj.name for obj in st.session_state.transport_objs],
# 		"Quantity": st.session_state.transport_quantity
# 	})

# 	st.subheader("Materials")
# 	st.dataframe(materials_df)

# 	st.subheader("Transports")
# 	st.dataframe(transports_df)