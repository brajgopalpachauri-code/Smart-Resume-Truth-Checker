import streamlit as st
from PyPDF2 import PdfReader
from skill_extractor import extract_skills
from questions import questions

from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(score, total, result):

    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    p.drawString(100, 800, "Resume Assessment Report")
    p.drawString(100, 760, f"Score: {score}/{total}")
    p.drawString(100, 730, f"Authenticity Score: {result:.2f}%")

    if result >= 80:
        status = "Resume Looks Genuine"
    elif result >= 50:
        status = "Partially Verified"
    else:
        status = "Needs Verification"

    p.drawString(100, 700, f"Status: {status}")

    p.save()

    buffer.seek(0)

    return buffer



st.title("Smart Resume Truth Checker")
st.markdown("___")
st.markdown("AI Powered Resume Verification")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type="pdf"
)

if uploaded_file:
    with st.spinner("Analyzing Resume..."):

     pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        text += page.extract_text()

    skills = extract_skills(text)
    st.success("Resume Analysis Complete!")    

    st.write("Skills Found:")
    st.write(skills)

    score = 0
    total = 0
    progress=st.progress(0)

    for skill in skills:
        progress_value=skills.index(skill)+1
        progress.progress(progress_value/len(skills))

        if skill in questions:

            st.subheader(skill.upper())

            for q, correct_answer in questions[skill].items():

                answer = st.text_input(q,key=f"{skills}_{q}")

                if answer:

                    total += 1

                    if correct_answer.lower() in answer.lower():
                        score += 1
    submit=st.button("Submit Answer")

    if submit and total > 0:

        result = (score / total) * 100

        st.write("Score =", score)
        st.write("Total =", total)

        st.metric(
       
       label="Skill Authenticity Score",
       value=f"{result:2f}%"
       
       )
        pdf_file = generate_pdf(score, total, result)

        st.download_button(
          "📄 Download Report",
          pdf_file,
          file_name="resume_report.pdf",
          mime="application/pdf"
     )
        
        if result>=80:
            st.success("Resume is likely authentic.")
        elif result>=50:
            st.warning("Resume is partially authentic.")
        else:
            st.error("Skills Need Verifcation.")

   