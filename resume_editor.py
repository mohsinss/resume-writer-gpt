import openai
import os
import streamlit as st
from dotenv import load_dotenv
from collections import Counter
import re

load_dotenv()
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import os

def extract_keywords(text, top_n=40):
    # Remove special characters and digits, and convert the text to lowercase
    clean_text = re.sub(r'[^\w\s]', '', text).lower()

    # Tokenize the text
    words = clean_text.split()

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Get the top_n keywords
    keywords = [word for word, _ in word_counts.most_common(top_n)]

    return ', '.join(keywords)

def reword_resume(resume, job_description, keywords):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    messages = [
        {"role": "system", "content": "You are a helpful assistant that rewords resumes to match job descriptions."},
        {"role": "user", "content": f"Here is the resume:\n{resume}\n\nAnd the job description:\n{job_description}\n\nThe ATS keywords are:\n{keywords}\n\nPlease suggest how to reword the resume to better match the ATS keywords from the job description while maintaining the general language of the original resume."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    suggestions = response.choices[0].message['content'].strip()
    return suggestions

# Layout
st.set_page_config(page_title='Resume Editor', layout='wide')

# Sidebar
st.sidebar.header('Resume Editor')
resume = st.sidebar.text_area('Paste your resume here:')
job_description = st.sidebar.text_area('Paste the job description here:')
submit_button = st.sidebar.button('Submit')
st.sidebar.subheader('Top ATS Keywords')

if submit_button and resume and job_description:
    keywords = extract_keywords(job_description)
    st.sidebar.text_area('Top ATS Keywords', value=keywords, height=270)
    enhanced_resume = reword_resume(resume, job_description, keywords)
    st.header('Your Enhanced Resume')
    st.write(enhanced_resume)
else:
    st.sidebar.text_area('Top ATS Keywords', height=270)
    st.header('Your Enhanced Resume')








# Main area
# st.header('Your Enhanced Resume')
# enhanced_resume_area = st.empty()

# Handle form submission
if submit_button and resume and job_description:
    enhanced_resume = reword_resume(resume, job_description, keywords)

    enhanced_resume_area.write(enhanced_resume)
    keywords = extract_keywords(job_description)
    st.sidebar.text_area('Top ATS Keywords', value=keywords, height=270)



