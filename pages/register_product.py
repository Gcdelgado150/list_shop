import streamlit as st
import pandas as pd
from helpers.sidebar import create_sidebar
import time


create_sidebar()
st.title("Cadastrar um produto...")

df = pd.read_csv("data/products.csv")
df = df.sort_values(by="name")
cols = st.columns(3)

def define_category(c1, c2):
    if not c1:
        return c2
    elif not c2:
        return c1
    elif c1 and c2:
        return c1
    
with cols[0]:
    st.header("Conferir lista de produtos existentes", divider="orange")
    with st.container(border=True, height=400):
        for produto in df.name.unique():
            st.write(produto)
with cols[1]:
    nome_produto = st.text_input(label="Nome do produto", help="Insira o nome do produto com letra maíscula")

    c1, c2 = st.columns(2)

    with c1:
        categoria_do_produto = st.text_input(label="Nome da categoria", 
                                             help="Insira o nome da categoria com letra maíscula",
                                             value=None)
    with c2:
        lcategory = df.category.unique()
        lcategory.sort()
        categoria_do_produto2 = st.selectbox("Categoria existente", 
                                             options=lcategory,
                                             index=None,
                                             placeholder=lcategory[0]
                                             )


    if st.button("Adicionar"):
        if nome_produto and (categoria_do_produto or categoria_do_produto2):

            if nome_produto not in df.name.unique():
                d = {"name": nome_produto, "category": categoria_do_produto or categoria_do_produto2}

                df2 = pd.DataFrame(d, index=[0])

                df = pd.concat([df, df2])

                df.to_csv("data/products.csv", index=False)

                st.success("Produto adicionado!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Produto já existe!")
        else:
            st.warning("Defina o produto e a categoria primeiro!")
with cols[2]:
    pass

