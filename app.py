from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        image_parts = [
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multilanguage Invoice Extractor")

st.header("Gemini Application")
input = st.text_input("Input Prompt: ", key="input")
upload_file = st.file_uploader("Choose an image of invoice ", type=["jpg", "jpeg", "png"])

image=""
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="uploaded Image", use_column_width=True)

submit = st.button("Tell me about invoice")

input_prompt ="""
You are an export in understanding invoices. 
we will upload an image as invoice and you will habe to answer any question based on uploaded invoice image
"""

if submit:
    image_data = input_image_setup(upload_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is ")
    st.write(response)
