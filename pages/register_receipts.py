import streamlit as st
import pandas as pd
from helpers.sidebar import create_sidebar
import requests
import json
import time
import os
import numpy as np

create_sidebar()

# Define the folder path
folder_path = "data/receipts_img/"

def get_ocr_read(imageFile, image_filename_original):
    print(f"[OCR] Sending this image: {imageFile} to OCR")
    receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
    
    r = requests.post(receiptOcrEndpoint, data = { \
        'api_key': 'TEST',        # Use 'TEST' for testing purpose \
        'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
        'ref_no': 'ocr_python_123', # optional caller provided ref code \
        }, \
    files = {"file": imageFile})
    receipt_json = f"data/receipts_json/{image_filename_original.split('.')[0]}.json"
    
    result = json.loads(r.text)
    if not result["success"]:
        print(result["message"])
        print("[OCR] OCR Failed, interrupted and waiting another hour!")
        time.sleep(60*60)
        return receipt_json, False

    print(f"[OCR] Saving this json as readed OCR: {receipt_json}")
    with open(receipt_json, 'w') as f:
        json.dump(result, f)

    return receipt_json, True

st.title("Adicionar um Recibo de compras")
with st.container(border=True):
    # Initialize a streamlit file uploader widget.
    uploaded_file = st.file_uploader("Escolha um arquivo")

    # If user attempts to upload a file.
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        # Show the image filename and image.
        st.write(f'Recibo: {uploaded_file.name}')

        # Save the uploaded file to the specified folder
        with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
            f.write(bytes_data)
            
        receipt_json, bool_success = get_ocr_read(imageFile=bytes_data, image_filename_original=uploaded_file.name)

        if bool_success:
            st.success("OCR readed successfully!")
        else:
            st.warning("OCR readed failed!")
