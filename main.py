import streamlit as st
import fitz
import os
from openai import OpenAI
from dotenv import load_dotenv

# Static Variables
SOFT_SKILLS = ["Leadership", "Problem Solving", "Teamwork", "Time Management", "Creativity", "Critical Thinking", "Confidence", "Communication"]

PROGRAMMING_LANGUAGES = ['ABAP', 'ActionScript', 'Ada', 'Apex', 'Assembly', 'Bash', 'Batch', 'C#', 'C++', 'COBOL', 'CSS', 'Clojure', 'ColdFusion', 'D', 'Dart', 'Delphi', 'Eiffel', 'Elixir', 'Erlang', 'F#', 'Forth', 'Fortran', 'Go', 'Groovy', 'HTML', 'Haskell', 'Java', 'JavaScript', 'Julia', 'Kotlin', 'Lisp', 'Logo', 'Lua', 'Matlab', 'OCaml', 'Objective-C', 'PHP', 'PL/SQL', 'Pascal', 'Perl', 'PowerShell', 'Prolog', 'Python', 'R', 'Racket', 'Ruby', 'Rust', 'SQL', 'Scala', 'Scheme', 'Shell', 'Smalltalk', 'Swift', 'Tcl', 'Transact-SQL', 'TypeScript', 'VHDL', 'Verilog', 'Visual Basic']

# Functions
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

def summarize_resume(text, client, softskill_criteria, promgramming_language_criteria):
    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": f"""You're a bot that is a HR for a tech company that is recruiting candidates for a Software Engineering position.
            You will look at the candidate's resume and give a summary of the candidate in 100 words.
            
            Also list out any softskill criteria that matches from this list: {softskill_criteria}
            
            Also list out any programming languages that matches from this list: {promgramming_language_criteria}
            """
        }, {
            "role": "user",
            "content": f"{text}"
        }],
        max_tokens=400,
        temperature=0.8
    )

    return summary_response


def main():
    st.title("Summarise Resume")
    softskill_options = st.multiselect("Select the soft-skills required for the job position", SOFT_SKILLS)
    programming_languages_options = st.multiselect("Select the programming languages required for the job position", PROGRAMMING_LANGUAGES)
    uploaded_file = st.file_uploader("Upload a Resume", type=["pdf"])


    if uploaded_file:
        # save the uploaded file in a directory
        save_uploaded_file(uploaded_file)
        if st.button("Generate Resume Summary"):
            text = extract_text_from_pdf(uploaded_file.name)
            summary = summarize_resume(text, client, softskill_options, programming_languages_options)
            st.write(summary.choices[0].message.content)


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))
    main()
    