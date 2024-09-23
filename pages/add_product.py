import streamlit as st
import pandas as pd
from helpers.sidebar import create_sidebar
from datetime import datetime
import os

today =  datetime.now().day
create_sidebar()

df = pd.read_csv("data/products.csv")

if os.path.isfile(f"data/lista_{today}.csv"):
    if st.button("Clear current list"):
        df_clear = pd.DataFrame({"name": [], "category": []})
        df_clear.to_csv(f"data/lista_{today}.csv", index=False)
        st.success("Current list cleared!")

cols = st.columns(2)

with cols[0]:
    nome_produto = st.selectbox(label="Escolha o produto", 
                                options=df.name.unique())
    
with cols[1]:
    if nome_produto:
        categoria_do_produto = df[df["name"] == nome_produto].category.unique()[0]
        st.write(categoria_do_produto)

if st.button("Adicionar à lista de compras"):
        save = True
        d = {"name": nome_produto, "category": categoria_do_produto}

        df2 = pd.DataFrame(d, index=[0])

        if os.path.isfile(f"data/lista_{today}.csv"):
             df = pd.read_csv(f"data/lista_{today}.csv")

             if nome_produto in df.name.unique():
                  st.warning("Produto já existe na lista!")
                  save = False

             df2 = pd.concat([df2, df])

        if save:
            df2.to_csv(f"data/lista_{today}.csv", index=False)
            st.success(f"Produto adicionado à lista do dia {today}!")
             
