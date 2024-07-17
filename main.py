import streamlit as st
import fitz
import os
from openai import OpenAI
from dotenv import load_dotenv

def save_uploaded_file(uploaded_file):
    SAVE_PATH = "./resume/"
    try:
        with open(os.path.join(SAVE_PATH, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getvalue())
        return True
    except Exception as e:
        print(e)
        return False

def extract_text_from_pdf(filename):
    doc = fitz.open(f"./resume/{filename}")
    text = ""
    for page in doc:
        text += page.get_text()
    
    return text

def summarize_resume(text, client):
    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": """You're a bot that is a HR for a tech company that is recruiting candidates for a Software Engineering position.
            You will look at the candidate's resume and give a summary of the candidate in 100 words. Also list out any criteria that matches
            from this list:
            [Python, Java, Javascript]"""
        }, {
            "role": "user",
            "content": f"{text}"
        }],
        max_tokens=400,
        temperature=0.8
    )

    return summary_response


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))
    st.title("Revolutinising Recruiment with AI")
    uploaded_file = st.file_uploader("Upload a Resume", type=["pdf"])

    if uploaded_file:
        # save the uploaded file in a directory
        save_uploaded_file(uploaded_file)
        text = extract_text_from_pdf(uploaded_file.name)
        summary = summarize_resume(text, client)
        st.write(summary.choices[0].message.content)