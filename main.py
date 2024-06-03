import streamlit as st
from pdfminer.high_level import extract_text
import requests
import os

# Gemini API key configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Ensure you set your Gemini API key as an environment variable

# Function to extract text from PDF
def extract_text_from_pdf(file):
    return extract_text(file)

# Function to chat with the text using Gemini's language model
def chat_with_text(text, user_input):
    response = requests.post(
        'https://api.gemini.com/v1/your-endpoint',  # Replace with the actual Gemini API endpoint
        headers={'Authorization': f'Bearer {GEMINI_API_KEY}'},
        json={
            'prompt': f"The following is the content of a PDF:\n\n{text}\n\nUser: {user_input}\nAssistant:",
            'max_tokens': 150
        }
    )
    response_data = response.json()
    return response_data['choices'][0]['text'].strip()  # Adjust based on the actual response structure

# Streamlit UI
st.title("Chat with your PDF")
st.write("Upload a PDF file to start chatting with its content.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("Text extracted from PDF successfully!")

    user_input = st.text_input("Ask something about the PDF content:")

    if st.button("Submit"):
        if user_input:
            with st.spinner("Getting response..."):
                response = chat_with_text(pdf_text, user_input)
            st.write("Assistant:", response)
        else:
            st.error("Please enter a question.")
