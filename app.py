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
    skill_scores={}
    skill_totals={}
    progress=st.progress(0)

    for skill in skills:
        progress_value=skills.index(skill)+1
        progress.progress(progress_value/len(skills))

        if skill in questions:
            skill_scores[skill]=0
            skill_totals[skill]=0

            st.subheader(skill.upper())

            for q, correct_answer in questions[skill].items():

                answer = st.text_input(q,key=f"{skill}_{q}")

                if answer:

                    total += 1
                    skill_totals[skill]+=1

                    if correct_answer.lower() in answer.lower():
                        score += 1
                        skill_scores[skill]+=1
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
        skill_feedback = ""
        
       
        if result >= 80:
                feedback = """
                Excellent! Your resume skills appear genuine.
                You have demonstrated strong knowledge in the selected skills.
                """
        elif result >= 50:
                feedback = """
                Your skills seem partially verified.
                Some concepts need improvement before interviews.
                """
        else:
                feedback = """
                Many skills could not be verified.
                More practice and revision is recommended.
                """
    skill_feedback = ""

               

    for skill in skill_scores:
        

        if skill_totals[skill] > 0:

            percentage = (skill_scores[skill] / skill_totals[skill]) * 100

            if percentage >= 80:
                skill_feedback += f"✅ {skill}: Excellent performance.\n\n"

            elif percentage >= 50:
                skill_feedback += f"⚠️ {skill}: Good but needs improvement.\n\n"

            else:
                skill_feedback += f"❌ {skill}: Needs more practice.\n\n"

            st.subheader("Skill Wise Analysis")
            st.info(skill_feedback)

            st.subheader("AI Feedback")
            st.info(feedback)
    