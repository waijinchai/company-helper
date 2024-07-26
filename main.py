import streamlit as st
# import fitz
import os
from openai import OpenAI
from dotenv import load_dotenv
from st_pages import Page, show_pages, add_page_title
import re
import ast

# CSS Style
button_style = """
    <style>
    .custom-button {
        color: white;
        background-color: transparent;
        padding: 10px 20px;
        border: 2px solid #33709C;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin-top: -1em;
    }
    .custom-button:hover {
        background-color: rgba(51, 112, 156, 0.5);
    }
    </style>
"""

custom_blue_button = """
    <style>
    .custom-blue-button {
        color: white;
        background-color: transparent;
        border: 1px solid white;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        padding: 0.5em;
        margin-top: -1em;
    }
    .custom-blue-button:hover {
        color: #A8D9E8;
        border: 1px solid #A8D9E8;
    }
    </style>
"""

tag_style = """
    <style>
    .tag {
        background-color: #e0e0e0;
        color: #333;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 5px;
        font-size: 12px;
        display: inline-block;
    }
    </style>
"""

# Theme
custom_green_color = "#8ed470"
custom_yellow_color = "#d6ca83"
custom_red_color = "#D48585"
custom_grey_color = "#EFF1F2"

# Variables
selected_job_title = ""
selected_soft_skills = []
selected_technical_skills = []

# Static Variables
SOFT_SKILLS = ["Leadership", "Problem Solving", "Teamwork", "Time Management", "Creativity", "Critical Thinking", "Confidence", "Communication"]

PROGRAMMING_LANGUAGES = ['ABAP', 'ActionScript', 'Ada', 'Apex', 'Assembly', 'Bash', 'Batch', 'C#', 'C++', 'COBOL', 'CSS', 'Clojure', 'ColdFusion', 'D', 'Dart', 'Delphi', 'Eiffel', 'Elixir', 'Erlang', 'F#', 'Forth', 'Fortran', 'Go', 'Groovy', 'HTML', 'Haskell', 'Java', 'JavaScript', 'Julia', 'Kotlin', 'Lisp', 'Logo', 'Lua', 'Matlab', 'OCaml', 'Objective-C', 'PHP', 'PL/SQL', 'Pascal', 'Perl', 'PowerShell', 'Prolog', 'Python', 'R', 'Racket', 'Ruby', 'Rust', 'SQL', 'Scala', 'Scheme', 'Shell', 'Smalltalk', 'Swift', 'Tcl', 'Transact-SQL', 'TypeScript', 'VHDL', 'Verilog', 'Visual Basic']

ROLE_DATA = [
    {
        "role": "Software Engineer (Junior)",
        "starting_date": "2024-07-02",
        "status": "Open"
    },
    {
        "role": "Finance Assistant",
        "starting_date": "2024-06-24",
        "status": "Open"
    },
    {
        "role": "Network Engineer",
        "starting_date": "2024-05-01",
        "status": "Close"
    },
    ]

CANDIDATES_DATA = []

JOB_DATA = []

ROLE = None

JOB_DESCRIPTION = """
Role Description:
We are seeking talented & motivated engineers to join our team! In this role, you'll delve into identity and access management, 
gaining practical experience within specific verticals such as Transportation, Food, and more. 
Your focus will be on analyzing, enhancing and safeguarding identity systems.
Day-to-Day Activities:
You use technology to solve well defined problems, building individual components or features based on well defined tasks. 
You understand the requirements of your projects and use that understanding in your designs. 
You understand your codebase and systems, ensuring reliability through design reviews, monitoring, alerting, and applying OE (Operational Excellence) standards. 
You take ownership of your code and ensure it's readable, maintainable, and well-tested. 
You understand and apply the appropriate data structures and algorithms. 
You give clear, actionable feedback during code reviews and respond well to feedback from others.
You respond promptly to issues and keep the working team constantly updated. 
Your tasks are delivered on time and with high quality, and you're able to explain your solutions to other technical stakeholders through both verbal and written communication.
Requirements:
- Experience with backend in Golang (preferred), Java, C# or any similar programming languages
- Strong computer science fundamentals including data structures and algorithms
- Strong communication skill both written and verbal
Extra:
- Experience in the IAM domain
- Experience with distributed systems in a cloud based environment
- Hunger to learn fast with a steep learning curve"""


soft_skills = ""
technical_skills = ""
current_job_description = ""

# Functions
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
            "content": f"Generate a job description for the job title: {job_title} and the job requirement: {job_requirement}"
        }
        ],
        max_tokens=500,
        temperature=0.8
    )

    return job_description_response

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
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": f"""You're a bot that is a HR for a tech company that is recruiting candidates for a Software Engineering position.
            You will look at the candidate's resume and give a summary of the candidate in 100 words.
            
            First list out the name of the candidate and then give a brief summary of the candidate's resume.

            Only list out the softskill criteria of the candidates that matches from this list: {softskill_criteria}
            
            Only list out the programming languages of the candidates that matches from this list: {promgramming_language_criteria}
            """
        },
        {
            "role": "user",
            "content": """
Sum Ting Wong
+97-1920192857 | SumTingWong@gmail.com | LinkedIn
W.P. Kuala Lumpur, Malaysia
BRIEF INTRODUCTION
A Year 3 Semester 1 Bachelor of Computer Science in Advanced Computer Science student currently
studying in Monash University Malaysia. Has interests in algorithms, data structures and deep learning.
Capable of programming in different languages under various programming paradigms.
EDUCATION
Monash University Malaysia
Kuala Lumpur, Malaysia
Bachelor of Computer Science in Advanced Computer Science
Feb 2022 - June 2025
●CGPA: 3.963 / 4.0
●WAM: 88.643 / 100
KEY SKILLS AND KNOWLEDGES
●Java
●Python
●UiPath Studio Classic
●UiPath Studio Modern
●JavaScript / TypeScript
●Object Oriented Programming
●Knowledges in Three-Layer Neural Network
●Knowledges in Algorithms and Data Structures
●Fluent communication and writing skills in English and Mandarin
AWARDS AND ACHIEVEMENTS
●Monash High Achiever Award
●Monash Coding League 2023 Semester 1 Top 25 Team
●Best Performing Student In Image Processing Unit
TRAINING AND CERTIFICATES
●HSK Level 6
●IELTS Academic 8.0
●UiPath Academy Automation Developer Associate
WORK EXPERIENCES
Top Education
Kuala Lumpur, Malaysia
Technology Intern, Tutor
Dec 2022 - Feb 2023
●Assisted in the start of operations
●Launched the Scratch Programing Language course for Juniors of age 7-11 years old
●Designed the course structure of Scratch Programming Language for Juniors of age 7-11 years old
●Instructed Scratch Programming Language to students of age 7-11 years old
●Received 100% Positive Feedback from students
Random Comp Sdn. Bhd.
Selangor, Malaysia
Robotics Cognitive Automation Intern
Nov 2023 - Feb 2024
●Developed and implemented robot monitoring system to optimize robot performance monitoring
o
Utilized SQL queries to extract robot run time data from database
●Assisted in migrating legacy robots into new platforms
●Produced proof of concept for Python Scripting into UiPath robots
●
Monash University Malaysia
Selangor, Malaysia
MUMTEC Industrial Relation Officer
Nov 2023 - Feb 2024
●
PROJECTS
Image Processing
“A Level 3 elective unit in Monash University Malaysia which covers topics related to image processing
and neural networks”
Image Processing Project
●License Plate Characters Recognition:
o Constructed a Three-Layer Neural Network in a team of three for identifying characters on
license plates
o Achieved 100.00% accuracy on the testing data set of characters
o Achieved 98.55% accuracy on license plate characters recognition
"""
        },
        {
            "role": "assistant",
            "content": """
            Candidate: Sum Ting Wong

            Summary:
            Sum Ting Wong is a motivated and passionate Bachelor of Computer Science student with a high CGPA from Monash University Malaysia. With a strong focus on algorithms, data structures, and deep learning, Sum Ting Wong has hands-on experience in both frontend and backend development. Proficient in multiple programming languages such as Java, Python, JavaScript, and TypeScript, Sum Ting Wong has also demonstrated expertise in UiPath Studio Classic and Modern. Recognized with the Monash High Achiever Award and other accolades, Sum Ting Wong has also gained practical experience through internships, developing robotic monitoring systems, and teaching programming to younger students. Fluent in English and Mandarin, Sum Ting Wong possesses strong communication and writing skills.

            Softskill criteria: Time Management, Communication, Teamwork, Continuous Learning, Problem-Solving
            Programming languages: Python, Java, JavaScript, TypeScript
            """
        },
        {
            "role": "user",
            "content": f"{text}"
        }],
        max_tokens=400,
        temperature=0.8
    )

    return summary_response

def extract_skills(prompt, client):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": """Based on the job description given, you will extract the soft skills and programming skills required 
            for the job position in an array of strings using the following steps:
            1. Extract the soft skills required for the job in json array of strings
            2. Extract the programming skills required for the job in json array of strings"""
        }, {
            "role": "user",
            "content": f"{JOB_DESCRIPTION}"
        },
        {
            "role": "assistant",
            "content": """["Critical Thinking", "Communication", "Problem Solving"]\n["Golang", "Java", "C#"]"""
        }, {
            "role": "user",
            "content": f"{prompt}"
        }],
        max_tokens=100,
        temperature=0.8
    )

    return response

# Component Rendering
def main():
    st.title("Revolutionizing Recruitment with AI")
    st.text("Reshaping the future of hiring and talent acquisition")

def show_job_listing():
    job_list_container = st.container(border=True)
    job_list_container.header("Job Listing")
    for item in ROLE_DATA:
        role, date, status = job_list_container.columns([2, 1, 1], gap="large", vertical_alignment="top")
        
        date.text(item["starting_date"])
        status.text(item["status"])
        role.markdown(button_style, unsafe_allow_html=True)

        if role.markdown(f'<button class="custom-button">{item["role"]}</button>', unsafe_allow_html=True):
            ROLE = item["role"]  

def get_local_data():
    job_desc = ""
    skills = ""
    job_title = ""

    with open('job_desc.txt', 'r') as file:
        job_desc = file.read()
    
    with open('skills.txt', 'r') as file:
        skills = file.read()
        skills = skills.split("\n")
        soft_skills = skills[0]
        technical_skills = skills[1]


    with open('job_title.txt', 'r') as file:
        job_title = file.read()
    
    return job_desc, soft_skills, technical_skills, job_title

def show_matching_candidates():

    job_desc, soft_skills, technical_skills, selected_job_title = get_local_data()

    st.title("Matching Candidates")
    st.text("How well does each candidates perform against the job description: ")
    st.text(job_desc)
    
    if st.button("Show Candidates"):
        st.header(selected_job_title)
        filenames = []

        directory = os.path.join(os.getcwd(), "resume")
        for filename in os.listdir(directory):
            filenames.append(filename)
        generate_all_resume_data(filenames, soft_skills, technical_skills, job_desc)

def matching_candidates(candidates_data):
    
    title_header, summary_header, match_header = st.columns([2, 1, 1], gap="large", vertical_alignment="top")
    title_header.markdown("<h1 style='font-size: 22px;'>Candidates Name</h1>", unsafe_allow_html=True)
    summary_header.markdown("<h1 style='font-size: 22px;'>Summary</h1>", unsafe_allow_html=True)
    match_header.markdown("<h1 style='font-size: 22px;'>Match</h1>", unsafe_allow_html=True)
    
    candidates_data_sorted = sorted(candidates_data, key=lambda x: x["matching_percentage"], reverse=True)

    for candidate in candidates_data_sorted:
        candidate_name, candidate_summary, match_percentage = st.columns([2, 1, 1], gap="large", vertical_alignment="top")
        candidate_name.markdown(f"<h2 style='font-size: 18px;'>{candidate['name']}</h2>", unsafe_allow_html=True)
        candidate_summary.button("🔗Summary", key=candidate["name"])
        
        tag_color = custom_red_color
        percentage = candidate["matching_percentage"]
        if percentage >= 80:
            tag_color = custom_green_color
        
        elif percentage >= 50:
            tag_color = custom_yellow_color
        
        match_percentage.markdown(f"<span style='border: 2px solid {tag_color}; color: {tag_color}; padding: 0.5em 0.8em; border-radius: 0.5em; font-weight: bold;'>\
                                    ★ {str(percentage)}%\
                                    </span>", unsafe_allow_html=True)

        with st.expander("Details"):
            st.markdown(f"<h3 style='font-size: 15px;'>Summary</h3>", unsafe_allow_html=True)
            st.write(candidate["resume_summary"])

            st.markdown(f"<h3 style='font-size: 15px;'>Matching Criteria</h3>", unsafe_allow_html=True)
            
            st.markdown("""
                <style>
                    .flex-container {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 10px;
                        margin-top: -20px;
                        margin-bottom: 20px;
                    }
                    .skill-tag {
                        border: 2px solid;
                        padding: 0em 0.8em;
                        border-radius: 0.5em;
                    }
                </style>
            """, unsafe_allow_html=True)

            flex_container = "<div class='flex-container'>"
 
            print(candidate["matching_criteria"])
            for skill in candidate["matching_criteria"]:
                flex_container += f"<span class='skill-tag' style='border-color: {custom_yellow_color}; color: white;'> {skill}</span>"

            flex_container += "</div>"

            st.markdown(flex_container, unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='font-size: 15px;'>Attachment</h3>", unsafe_allow_html=True)

            st.markdown(custom_blue_button, unsafe_allow_html=True)
            st.markdown(f'<button class="custom-blue-button">🔗Resume</button>', unsafe_allow_html=True)
        st.divider()

def new_position():
    st.title("Create New Position")
    st.text("AI-powered tool to generate Job Description instantly")
    
    soft_skills = []
    technical_skills = []
    current_job_description = ""

    with st.form("Create New Position"):
        job_title = st.text_input("Job Title:")
        job_requirement = st.text_input("Job Requirement:")
        submit_button = st.form_submit_button("Generate Job Description")

        if submit_button:
            st.header("Generated Job Description")
            current_job_description = st.text_area(
                label="",
                value=generate_job_description(job_title, job_requirement, client).choices[0].message.content,
                # value="Hello",
                height=400,
            )
            
            skills_response = extract_skills(current_job_description, client)
            skills = skills_response.choices[0].message.content.split("\n")
            # skills = [["Critical Thinking, Communication, Problem Solving"], ["Golang, Java, C#"]]
            soft_skills = skills[0]
            technical_skills = skills[1]
            JOB_DATA.append({
                "job_title": job_title,
                "job_requirement": job_requirement,
                "soft_skills": soft_skills,
                "technical_skills": technical_skills
            })

            save_job_title(job_title)
            save_job_description(current_job_description)
            save_skills(soft_skills, technical_skills)
    show_matching_candidates()

def save_job_description(job_desc):
    with open('job_desc.txt', 'w') as file:
        file.write(job_desc)

def save_skills(soft_skills, technical_skills):
    with open('skills.txt', 'w') as file:
        file.write(str(soft_skills) + "\n" + str(technical_skills))

def save_job_title(job_title):
    with open('job_title.txt', 'w') as file:
        file.write(job_title)

def save_resume_to_db(uploaded_file):
    """
    Function that saves the resume to the database
    """
    # Specify the path where you want to save the file
    save_path = f"./resume/{uploaded_file.name}"

    # Save the uploaded file to the specified path
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved successfully to database")

def upload_resume():
    """
    Function that uploads the resume to the database
    """
    st.title("Upload A Resume")
    st.text("Upload a resume into the system")

    uploaded_file = st.file_uploader("Upload a Resume", type=["pdf"], accept_multiple_files=True)

    if uploaded_file:
        for file in uploaded_file:    
            # Save the file to the database
            save_resume_to_db(file)


def generate_all_resume_data(resumes, soft_skills, technical_skills, job_desc):
    """
    Given all of the resumes
    1. Extract text from the resume
    2. Summarize the resume
    3. Generate matching score
    4. Insert all of the data into the database
    """
    client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))
    index = 0
    for resume in resumes:
        resume_text = extract_text_from_pdf(resume)
        resume_summary_response = summarize_resume(resume_text, client, soft_skills, technical_skills)
        name, resume_summary, matching_criteria = preprocess_resume_response_data(resume_summary_response)
        score = generate_matching_score(job_desc, client, soft_skills, technical_skills, resume_text)
        score_output = ast.literal_eval(score.choices[0].message.content)

        candidate_data = {
            "name": name,
            "resume_summary": resume_summary,
            "matching_criteria": matching_criteria,
            "matching_percentage": next(iter(score_output.values()))
        }
        insert_candidate_data(candidate_data)
        index += 1
    matching_candidates(CANDIDATES_DATA)

def insert_candidate_data(candidate_data):
    """
    insert all candidate data into the database
    """
    CANDIDATES_DATA.append(candidate_data)

def preprocess_resume_response_data(resume_response):
    candidate_string = resume_response.choices[0].message.content
    inputs = candidate_string.split("\n")
    # print(f"Inputs --> {inputs}")

    # Extract the name
    name_pattern = r"Candidate:\s*(.*)"
    name_match = re.search(name_pattern, candidate_string)
    name = name_match.group(1).strip() if name_match else None

    # Extract the summary
    summary_pattern = r"Summary:\s*(.*?)\s*Softskill criteria:"
    summary_match = re.search(summary_pattern, candidate_string, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else None

    # Extract the soft skills
    soft_skills_pattern = r"Softskill criteria:\s*(.*?)\s*Programming languages:"
    soft_skills_match = re.search(soft_skills_pattern, candidate_string, re.DOTALL)
    soft_skills = [skill.strip() for skill in soft_skills_match.group(1).split(',')] if soft_skills_match else []

    # Extract the programming languages
    programming_languages_pattern = r"Programming languages:\s*(.*)"
    programming_languages_match = re.search(programming_languages_pattern, candidate_string)
    programming_languages = [lang.strip() for lang in programming_languages_match.group(1).split(',')] if programming_languages_match else []
    
    for input_str in programming_languages:
        if "None" in input_str:
            programming_languages = []
            break
    return name, summary, soft_skills + programming_languages
    
def generate_matching_score(job_description, client, softskill_criteria, promgramming_language_criteria, *resumes):
    summary_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": f"""You're a bot that is a HR for a tech company that is recruiting candidates for a Software Engineering position.
            You will analyze the following candidate resumes and generate a job matching percentage based on the given job description,
            soft skill criteria, and programming language criteria.
            job_description: {job_description}
            softskill_criteria: {softskill_criteria}
            programming_language_criteria: {promgramming_language_criteria}

            Return the matching score ranging from 0 to 100 according to the number of resumes provided and in the same order as the resumes provided as json with the candidate's name as the key and the matching score as the value. Do not include any tags in the output.
            """
        },
        { "role": "user", "content": """("Sum Ting Wong
+97-1920192857 | SumTingWong@gmail.com | LinkedIn
W.P. Kuala Lumpur, Malaysia
BRIEF INTRODUCTION
A Year 3 Semester 1 Bachelor of Computer Science in Advanced Computer Science student currently
studying in Monash University Malaysia. Has interests in algorithms, data structures and deep learning.
Capable of programming in different languages under various programming paradigms.
EDUCATION
Monash University Malaysia
Kuala Lumpur, Malaysia
Bachelor of Computer Science in Advanced Computer Science
Feb 2022 - June 2025
●CGPA: 3.963 / 4.0
●WAM: 88.643 / 100
KEY SKILLS AND KNOWLEDGES
●Java
●Python
●UiPath Studio Classic
●UiPath Studio Modern
●JavaScript / TypeScript
●Object Oriented Programming
●Knowledges in Three-Layer Neural Network
●Knowledges in Algorithms and Data Structures
●Fluent communication and writing skills in English and Mandarin
AWARDS AND ACHIEVEMENTS
●Monash High Achiever Award
●Monash Coding League 2023 Semester 1 Top 25 Team
●Best Performing Student In Image Processing Unit
TRAINING AND CERTIFICATES
●HSK Level 6
●IELTS Academic 8.0
●UiPath Academy Automation Developer Associate
WORK EXPERIENCES
Top Education
Kuala Lumpur, Malaysia
Technology Intern, Tutor
Dec 2022 - Feb 2023
●Assisted in the start of operations
●Launched the Scratch Programing Language course for Juniors of age 7-11 years old
●Designed the course structure of Scratch Programming Language for Juniors of age 7-11 years old
●Instructed Scratch Programming Language to students of age 7-11 years old
●Received 100% Positive Feedback from students
Random Comp Sdn. Bhd.
Selangor, Malaysia
Robotics Cognitive Automation Intern
Nov 2023 - Feb 2024
●Developed and implemented robot monitoring system to optimize robot performance monitoring
o
Utilized SQL queries to extract robot run time data from database
●Assisted in migrating legacy robots into new platforms
●Produced proof of concept for Python Scripting into UiPath robots
●
Monash University Malaysia
Selangor, Malaysia
MUMTEC Industrial Relation Officer
Nov 2023 - Feb 2024
●
PROJECTS
Image Processing
“A Level 3 elective unit in Monash University Malaysia which covers topics related to image processing
and neural networks”
Image Processing Project
●License Plate Characters Recognition:
o Constructed a Three-Layer Neural Network in a team of three for identifying characters on
license plates
o Achieved 100.00% accuracy on the testing data set of characters
o Achieved 98.55% accuracy on license plate characters recognition", "Kishma Dnutts
Address: Selangor, Malaysia
Contacts: +9182 192 1098 | KishmaDnutts@gmail.com | https://www.linkedin.com/in/KishDnuttsPlz/
Education
Monash University
Bachelor of Computer Science in Advanced Computer Science
Feb 2022 – June 2025
●
CGPA: 3.934 / 4.00
●
Weighted Average Mark (WAM): 85.844 / 100.0
Experience
Super Tech Sdn Bhd
Software Engineer Intern
Nov 2023 - Feb 2024
●
Developed 3 RESTful API with Python FAST API to facilitate communication between two backend system
●
Implemented a backend process for handling & processing the API requests with Python & SQL
●
Designed comprehensive test cases to test RESTful APIs and crucial functionalities of the backend process
●
Built a Extract, Transform, Load (ETL) data pipeline for a data migration project in Python & SQL
●
Collaborated with 2 other developers and resolved over 700 DAG compilation errors within an established
Apache Airflow infrastructure
●
Facilitated a seamless migration of DAGs to the client’s production environment
●
Assisted in documentation such as Design Documents, System Integration Testing Document
University Coursework
Database - Community Cleaning & Holiday Resort Management System
SQL, MongoDB, Git
●
Led a group of 3 to design & implement a relational database for a Community Cleaning System with UML
●
Performed common relational database operations given an existing database to meet user requirements
●
Developed and used PL/SQL to enforce business rules and data integrity
Object Oriented Programming & Design
Java, Git || Elden Ring || Fiery Dragon
●
Applied suitable object-oriented design principles & design patterns to produce quality codebase
●
Modelled and designed flexible software architectures based on user requirements
●
Iteratively analysed and refactored existing software systems to improve quality of code and software
Technical Skills
●
Programming Languages: Python, Java, SQL
●
Databases: Oracle SQL, MYSQL, MongoDB, Firebase
●
Frontend: HTML, CSS & JavaScript, React, TypeScript
●
Tools: Git
Awards & Extracurricular Activities
Monash University Malaysia Technology Club (MUMTEC)
MUMTEC
Head of Industrial Relation
Feb 2024 - Dec 2024
●
Led a team of 4 in identifying and liaising with industrial partners, securing event sponsorships, and
coordinating events for MUMTEC
Competitive Programming Competitions & Hackathons
●
Participated in Vhack USM 2023 – hosted by University Sains Malaysia
●
4th Place in Nott-A-Thon: Lovelace Competitive Programming Competition 2022 – by Nottingham Malaysia
●
Top 50 in Monash Coding League 2023 – hosted by School of Information Technology, Monash University
References
Soo Loo Boo
Senior Manager (Software Development), Super Tech Sdn Bhd
+7891 019 3019")""" },
        { "role": "assistant", "content": """
         {"Sum Ting Wong": 85,"Kishma Dnutts": 90}
         """ },
        {
            "role": "user",
            "content": f"{resumes}"
        }],
        max_tokens=400,
        temperature=0.8
    )

    return summary_response    


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))
    main()

    new_position()
    upload_resume()
    # show_matching_candidates()