import streamlit as st

def create_sidebar():
    st.set_page_config(layout="wide")

    st.sidebar.image("data/logo.jpg")
    st.sidebar.title("Produtos")
    st.sidebar.page_link("home.py", label="Produtos cadastrados")
    st.sidebar.page_link("pages/register_product.py", label="Registrar um produto")

    st.sidebar.divider()
    st.sidebar.header("Lista de compras...")
    st.sidebar.page_link("pages/add_product.py", label="Adicionar um produto à lista")
    st.sidebar.page_link("pages/check_list.py", label="Checar lista de compras")
    
    st.sidebar.divider()
    st.sidebar.header("Recibos")
    st.sidebar.page_link("pages/register_receipts.py", label="Adicionar um recibo de compra")
    st.sidebar.page_link("pages/check_receipts.py", label="Conferir recibos de compra")