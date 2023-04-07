import openai
import os
import streamlit as st
from dotenv import load_dotenv
from collections import Counter
import re

load_dotenv()

def extract_keywords(text, top_n=40):
    excluded_words = {
        'and', 'to', 'in', 'the', 'of', 'with', 'our', 'for',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'that', 'will', 'would', 'could', 'have', 'has', 'had',
        'it', 'we', 'them', 'they', 'are', 'been', 'or', 'as',
        'what', 'them', 'their', 'so'
    }
    clean_text = re.sub(r'[^\w\s]', '', text).lower()
    words = clean_text.split()
    word_counts = Counter(words)
    keywords = [word for word, _ in word_counts.most_common() if word not in excluded_words]

    return ', '.join(keywords[:top_n])
def main_area():
    st.markdown(
        """
        <style>
        .a4_textarea {
            border: 3px solid #ADD8E6;
            box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.25);
            height: 1123px;
            width: 794px;
            padding: 20px;
            margin: 0 auto;
            background-color: white;
        }
        .top_bar {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background-color: #ADD8E6;
            padding: 10px;
            margin-bottom: 10px;
        }
        .top_bar button {
            box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.15);
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.write('<div class="top_bar"><button class="top_bar button">Resume</button><button class="top_bar button">Cover Letter</button></div>', unsafe_allow_html=True)
    enhanced_resume = st.empty()
    st.write('<div class="a4_textarea">', unsafe_allow_html=True)
    enhanced_resume.markdown("", unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)
    return enhanced_resume

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

st.set_page_config(page_title='Resume Editor', layout='wide')

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
    main_area().markdown(enhanced_resume, unsafe_allow_html=True)
else:
    st.sidebar.text_area('Top ATS Keywords', height=270)
    st.header('Your Enhanced Resume')
    main_area()
