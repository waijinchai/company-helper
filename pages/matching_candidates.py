import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

def matching_candidates():
    st.title("Matching Candidates")
    
if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))
    matching_candidates()