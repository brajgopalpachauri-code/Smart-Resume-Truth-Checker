import streamlit as st
from PyPDF2 import PdfReader
from skill_extractor import extract_skills
from questions import questions

st.title("Smart Resume Truth Checker")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type="pdf"
)

if uploaded_file:

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        text += page.extract_text()

    skills = extract_skills(text)

    st.write("Skills Found:")
    st.write(skills)

    score = 0
    total = 0

    for skill in skills:

        if skill in questions:

            st.subheader(skill.upper())

            for q, correct_answer in questions[skill].items():

                answer = st.text_input(q)

                if answer:

                    total += 1

                    if correct_answer.lower() in answer.lower():
                        score += 1

    if total > 0:

        result = (score / total) * 100

        st.write("Score =", score)
        st.write("Total =", total)

        st.success(
        f"Skill Authenticity Score: {result:.2f}%"
       )
        if result>=80:
            st.success("Resume is likely authentic.")
        elif result>=50:
            st.warning("Resume is partially authentic.")
        else:
            st.error("Skills Need Verifcation.")
   