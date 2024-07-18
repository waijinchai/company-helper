import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

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

def new_position():
    st.title("Create New Position")
    st.write("AI-powered tool to generate Job Description instantly")
    job_title = st.text_input("Job Title:")
    job_requirement = st.text_input("Job Requirement:")

    if st.button("Generate Job Description"):
        st.text_area(
            label="Generated Job Description",
            value=generate_job_description(job_title, job_requirement, client).choices[0].message.content,
            height=400,
            max_chars=None,
            key=None
        )
        
if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_SECRET"))
    new_position()
