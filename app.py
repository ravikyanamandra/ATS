import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()  # load all environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""  # Corrected variable name from txt to text
    for page in reader.pages:  # Correct iteration over pages
        text += page.extract_text() or ""  # Added or "" to handle None return from extract_text
    return text

# Prompt Template
input_prompt_template = """
Hey, act like a skilled ATS (Application Tracking System) with a deep understanding of the tech field, including software engineering, data science, data analyst, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider that the job market is very competitive and you should provide the best assistance for improving the resumes. Assign the percentage match based on the job description and the missing keywords with high accuracy.
Resume: {text}
Description: {jd}

I want the response in one single string having the structure
{{"JD Match":"%","Missing Keywords":[],"Profile Summary":""}}
"""

## Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume for ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        formatted_prompt = input_prompt_template.format(text=text, jd=jd)  # Format the prompt with actual text and jd
        response = get_gemini_response(formatted_prompt)
        st.subheader("Response")
        st.write(response)
