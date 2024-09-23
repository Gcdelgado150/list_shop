import streamlit as st
import pandas as pd
from helpers.sidebar import create_sidebar

create_sidebar()

df = pd.read_csv("data/products.csv")

with st.container():
    st.title("Lista de produtos cadastrados...")
    new_df = st.data_editor(df[["name", "category"]], height=800, width=500, hide_index=True)
    new_df.to_csv("data/products.csv")