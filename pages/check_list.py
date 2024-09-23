import streamlit as st
import pandas as pd
from helpers.sidebar import create_sidebar
from datetime import datetime
import os

today = datetime.now().day
create_sidebar()

if os.path.isfile(f"data/lista_{today}.csv"):
    df = pd.read_csv(f"data/lista_{today}.csv")

    # Get unique categories
    categories = df.category.unique()

    # Calculate the number of rows needed (3 columns per row)
    num_rows = (len(categories) + 2) // 3  # Ceiling division to handle the last row

    # Iterate through rows and columns to create the layout
    for i in range(num_rows):
        # Create a row with 3 columns
        row_cols = st.columns(3)
        
        # Populate each column in the row
        for j in range(3):
            index = i * 3 + j
            if index < len(categories):
                category = categories[index]
                df_category = df[df["category"] == category]

                s = ""
                with row_cols[j].container(border=True):
                    st.write(category.capitalize())
                    
                    for name in df_category.name.unique():
                        s += "- " + name + "\n"

                    st.markdown(s)
            else:
                # If there are fewer categories than columns, leave empty
                with row_cols[j].container():
                    st.write("")  # or st.markdown("") to ensure the column has space

else:
    st.write(f"There is no list for today: {today}")