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

def generate_job_description(job_title, job_requirement, client):
    job_description_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": f"""
            You're a bot that is a HR for a company.
            This company is a tech company that specializes in software development for various clients.
            The company serves various industries from finance, agriculture, health, and many more.
            Some of the solutions that the company provides to the clients includes web development, mobile app development, and data analytics, artificial intelligence and many more.
            You would receive a vague job requirement from the tech team of the company.
            Based on the vague job title and the job requirement received, generate a detailed job description.
            """
        },
        {
            "role": "user",
            "content": f"Generate a job description for the job title: Senior Software Enginner, iOS and the job requirement: Expert in iOS development including the use of Swift and/or RxSwift."
        },
        {
            "role": "assistant",
            "content": f"""
Role Description:
As a Senior iOS Engineer in the Safety team, you will be responsible for designing and implementing Safety features in our iOS application. You will work on various aspects of Grab's Safety features which revolves around a wide variety of device hardwares and requires a deep understanding of not only application programming but also system performance.

This is a regional role where you'll have the opportunity to collaborate with a diverse cross-functional team of mobile and backend engineers, data scientists, product managers, and designers to deliver code behind apps that impact millions of lives in Southeast Asia.

Day to Day Activities:
- Take charge of executing and monitoring projects while collaborating with Product, Design, Mobile, and Backend teams to continuously improve and extend new consumer and/or partner-facing products, platforms, and features.
- Actively participate in technical and product review meetings, enhancing Grab platform's efficiency through the creation and optimization of reusable iOS software components.
- Drive continuous improvement on live apps by reviewing performance on both, the code and experience level, ensuring high-quality app releases.
- Foster cross-team collaborations to share knowledge, review each other's code, and assist in building an environment conducive to learning and growing.
- Embrace and promote cutting-edge mobile methodologies and technologies, and invest in the mentorship of Junior Engineers for their career development.

Requirements:
- Expert in iOS programming paradigms including extensive use of Swift and/or RxSwift.
- Demonstrate working knowledge of architectural approaches, design, caching, data storage, and security.
- Showcase a strong background in UI/UX design, ensuring intuitive functionality and pixel-perfect interfaces.
- Possess hands-on experience with unit testing, UI test frameworks, and continuous integration pipelines for mobile apps build systems.
- Exhibit strong Computer Science fundamentals, proven 'Your Problem Is My Problem' (YPIMP) teamwork attitude, and a relevant academic background i.e., Degree in Computer Science, Software Engineering, IT, or related fields.

Extra:
- Experience with iOS application performance tuning and optimisation.
- Experience with Machine Learning Model deployment and inference on-device.
        """
        },
        {
            "role": "user",
            "content": f"Generate a job description for the job title: {job_title}, iOS and the job requirement: {job_requirement}"
        }
        ],
        max_tokens=400,
        temperature=0.8
    )

    return job_description_response

def main():
    st.title("Revolutionising Recruiment with AI")
    job_title = st.text_input("Enter job title here")
    job_requirement = st.text_input("Enter job requirement here")

    if st.button("Generate Job Description"):
        st.text_area(
            label="Generated Job Description",
            value=generate_job_description(job_title, job_requirement, client).choices[0].message.content,
            height=400,
            max_chars=None,
            key=None
        )

    softskill_options = st.multiselect("Select the soft-skills required for the job position", SOFT_SKILLS)
    programming_languages_options = st.multiselect("Select the programming languages required for the job position", PROGRAMMING_LANGUAGES)
    uploaded_file = st.file_uploader("Upload a Resume", type=["pdf"])


    if uploaded_file:
        # save the uploaded file in a directory
        save_uploaded_file(uploaded_file)
        text = extract_text_from_pdf(uploaded_file.name)
        summary = summarize_resume(text, client, softskill_options, programming_languages_options)
        st.write(summary.choices[0].message.content)


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))
    main()
    