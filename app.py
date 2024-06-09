from dotenv import load_dotenv
load_dotenv()
import json

import streamlit as st
from streamlit_lottie import st_lottie  # pip install streamlit-lottie
import os
import sqlite3

import google.generativeai as genai




def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load google AI model
def get_gemini(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

## function to retrive quey from sql data
def get_sql_query(sql, db):
    conn=sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


# Defining the Prompt
prompt=[
    """
    You are an expert in converting English question to SQL query !
    The SQL database has the name STUDENT and has the following columns:
    NAME, CLASS, SECTION, MARKS \n\nFor example, if the question is 
    "What is the name of the student who scored the highest marks in Data Science?", 
    the SQL query would be "SELECT NAME FROM STUDENT WHERE CLASS='Data Science' ORDER BY MARKS DESC LIMIT 1;"
    \n\n Example-2: "What is the average marks of students in Data Science?"
    the SQL query would be "SELECT AVG(MARKS) FROM STUDENT WHERE CLASS='Data Science';"
    also the sql code should not have ``` in the beginning or end and sql word in the output


    """
]

# Streamlit App
lottie_coding = load_lottiefile("amine.json")  # link to local lottie file
st.set_page_config(page_title="I can Retreive any SQL query")
st.header("Gemini App to Query OMOPCDM Database")
st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=False,
    quality="high", # medium ; high
    height=None,
    width=None,
    key=None,
)


question = st.text_input("Enter your question here: ", key="input")

submit = st.button("Ask Gemini")

# If the submit button is clicked
if submit:
    response=get_gemini(question, prompt)
    print(response)
    data=get_sql_query(response, "student.db")
    st.subheader("The Response is:")
    for row in data:
        print(row)
        st.header(row)




# /home/jay-sanjay/Downloads/my/df.sqlite/
