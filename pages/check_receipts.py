
import streamlit as st
import pandas as pd
from helpers.sidebar import create_sidebar
import os
import json
import numpy as np

create_sidebar()
st.title("Conferir/editar um recibo...")

if len(os.listdir("data/receipts_json/")) > 0:
    for receipt_json in os.listdir("data/receipts_json/"):
        with st.expander(receipt_json):
            st.header(receipt_json)
            cols = st.columns([1, 2])

            with cols[0]:
                st.image("data/receipts_img/" + receipt_json.split(".")[0] + ".jpg", width=400)

            with open("data/receipts_json/" + receipt_json) as f:
                data = json.load(f)

            if not data["success"]:
                st.write(data["message"])
                continue
            date = data['receipts'][0]['date']
            filename = f"data/receipts_csv/{date}.csv"

            if os.path.isfile(filename):
                df = pd.read_csv(filename)
            
            else:
                d = {"Produto" : [], 
                    "Quantidade": [],
                    "Valor Unitário": [],
                    "Valor Total": [],
                    "Supermercado": []}

                for item in data["receipts"][0]["items"]:
                    d["Produto"].append(' '.join(item["description"].split(" ")[1:]))
                    d["Quantidade"].append(item["qty"])
                    d["Valor Unitário"].append(item["unitPrice"])
                    d["Valor Total"].append(item["amount"])
                    d["Supermercado"].append(data["receipts"][0]["merchant_name"])

                df = pd.DataFrame(d)

                # Fix values misreaded
                df['Quantidade'] = df['Valor Total']/df["Valor Unitário"]
                df["Quantidade"] = df["Quantidade"].fillna(1)
                df['Valor Unitário'] = np.round(df['Valor Total']/df["Quantidade"], 3)

                # Save dataframe
                df.to_csv(filename, index=False)

            with cols[1]:
                supermarket = st.text_input(label="Nome do supermercado", 
                                            value=None,
                                            placeholder=df.Supermercado.unique()[0])

                if supermarket:
                    df["Supermercado"] = supermarket

                new_df = st.data_editor(df, height=800, width=1000, hide_index=True)
                new_df.to_csv(filename, index=False)