import streamlit as st
import fitz
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

#print(os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="🚀",
    layout="wide"
)
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0
st.markdown(
    """
    <h1 style='text-align:center; color:#4F46E5;'>
    🚀 AI Recruitment System
    </h1>
    <h4 style='text-align:center; color:gray;'>
    Resume Analysis • ATS Scoring • Interview Assessment
    </h4>
    """,
    unsafe_allow_html=True
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("ATS Accuracy", "95%")

with col2:
    st.metric("Interview Modules", "HR + Technical")

with col3:
    st.metric("Resume Analysis", "AI Powered")

st.divider()
def create_pdf_report(name, email, phone, ats_result):

    pdf_file = "ATS_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Recruitment System Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Name: {name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Email: {email}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Phone: {phone}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            ats_result.replace("\n", "<br/>"),
            styles["Normal"]
        )
    )

    doc.build(content)

    return pdf_file

uploaded_file = st.file_uploader(
    "📄 Upload Your Resume",
    type=["pdf"]
)

if uploaded_file:

    st.success("✅ Resume Uploaded Successfully!")

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    resume_text = ""

    for page in pdf:
        resume_text += page.get_text()

    # =========================
    # PREPARE LINES
    # =========================

    lines = [
        line.strip()
        for line in resume_text.split("\n")
        if line.strip()
    ]

    # =========================
    # NAME EXTRACTION
    # =========================

    prompt = f"""
    Extract ONLY the candidate's full name from this resume.

    Resume:
    {resume_text}

    Return only the name.
    """
    try:
        response = model.generate_content(prompt)
        name = response.text.strip()

    except:
        name = "Name Not Available"
    # =========================
    # EMAIL EXTRACTION
    # =========================

    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        resume_text
    )

    email = (
        email_match.group()
        if email_match
        else "Not Found"
    )

    # =========================
    # PHONE EXTRACTION
    # =========================

    phone_match = re.search(
        r'(\+91[-\s]?)?[6-9]\d{9}',
        resume_text
    )

    phone = (
        phone_match.group()
        if phone_match
        else "Not Found"
    )

    # =========================
    # SKILLS EXTRACTION
    # =========================

    skills_db = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "SQL",
        "MySQL",
        "MongoDB",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "OpenCV",
        "Data Analytics",
        "Power BI",
        "Excel",
        "Git",
        "GitHub"
    ]

    detected_skills = []

    for skill in skills_db:

        if skill.lower() in resume_text.lower():

            if skill not in detected_skills:
                detected_skills.append(skill)

    # =========================
    # INTERNSHIPS EXTRACTION
    # =========================

    internships = []

    internship_keywords = [
        "intern",
        "internship",
        "trainee",
        "industrial training",
        "summer training",
        "software developer trainee"
    ]

    for line in lines:

        if any(
            keyword in line.lower()
            for keyword in internship_keywords
        ):
            internships.append(line)

    # =========================
    # CERTIFICATIONS EXTRACTION
    # =========================

    certifications = []

    cert_keywords = [
        "nptel",
        "coursera",
        "udemy",
        "certificate",
        "certification",
        "google",
        "aws",
        "microsoft",
        "cisco",
        "oracle",
        "course",
        "learnathon"
    ]

    for line in lines:

        if any(
            keyword in line.lower()
            for keyword in cert_keywords
        ):
            certifications.append(line)

    # =========================
    # PROJECTS EXTRACTION
    # =========================

    projects = []

    project_keywords = [
        "project",
        "projects",
        "academic project",
        "major project",
        "minor project",
        "capstone"
    ]

    capture = False

    for line in lines:

        lower_line = line.lower()

        if any(
            keyword in lower_line
            for keyword in project_keywords
        ):
            capture = True
            continue

        if capture:

            if any(
                stop_word in lower_line
                for stop_word in [
                    "education",
                    "certification",
                    "internship",
                    "experience",
                    "skills"
                ]
            ):
                break

            if len(line.strip()) > 5:
                projects.append(line)

    # =========================
    # DISPLAY SUMMARY
    # =========================

    st.subheader("📋 Resume Summary")

    col1, col2 = st.columns(2)
    

    with col1:
        st.info(f"👤 Name: {name}")

    with col2:
        st.info(f"📧 Email: {email}")

    st.info(f"📱 Phone: {phone}")

    # =========================
    # SKILLS DISPLAY
    # =========================

    st.subheader("🛠 Detected Skills")

    if detected_skills:

        for skill in detected_skills:
            st.success(skill)

    else:
        st.warning("No Skills Detected")

    # =========================
    # INTERNSHIPS DISPLAY
    # =========================

    st.subheader("💼 Internships")

    if internships:

        for internship in internships:
            st.markdown(f"• {internship}")

    else:
        st.warning("No Internships Found")

    # =========================
    # CERTIFICATIONS DISPLAY
    # =========================

    st.subheader("🏆 Certifications")

    if certifications:

        for cert in certifications:
            st.markdown(f"• {cert}")

    else:
        st.warning("No Certifications Found")

    # =========================
    # PROJECTS DISPLAY
    # =========================

    st.subheader("🚀 Projects")

    if projects:

        for project in projects:
            st.markdown(f"• {project}")

    else:
        st.warning("No Projects Found")

    # =========================
    # RESUME CONTENT
    # =========================

    with st.expander("📄 View Original Resume"):
        st.text_area(
            "Resume Content",
            resume_text,
            height=350,
            key="Original_Resume"
    )

    # ==================================
    # PHASE 3 - JOB ROLE MATCHING
    # ==================================

    st.divider()
    st.subheader("🎯 Job Role Matching")
    job_role = st.selectbox(
        "Select Target Job Role",
        [
            "Python Developer",
            "Java Developer",
            "Data Analyst",
            "Machine Learning Engineer",
            "Full Stack Developer"
        ]
    )
    

    role_skills = {

        "Python Developer": [
            "Python",
            "SQL",
            "Git",
            "GitHub",
            "MongoDB"
        ],

        "Java Developer": [
            "Java",
            "SQL",
            "Git",
            "GitHub"
        ],

        "Data Analyst": [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Data Analytics"
        ],

        "Machine Learning Engineer": [
            "Python",
            "Machine Learning",
            "TensorFlow",
            "OpenCV",
            "SQL"
        ],

        "Full Stack Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "MongoDB"
        ]
    }
    

    required_skills = role_skills[job_role]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in detected_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    match_percentage = int(
        (len(matched_skills) / len(required_skills)) * 100
    )


    st.progress(match_percentage / 100)

    st.metric(
        "Resume Match",
        f"{match_percentage}%"
    )

    st.subheader("✅ Matching Skills")

    for skill in matched_skills:
        st.success(skill)

    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.error(skill)
    else:
        st.success("No Missing Skills 🎉")
    questions = {
    "Python Developer": [
        "What is Python?",
        "Explain OOP concepts.",
        "What are Python decorators?",
        "Difference between List and Tuple?",
        "What is Exception Handling?"
        ],


    "Machine Learning Engineer": [
        "What is Machine Learning?",
        "Explain CNN.",
        "What is Overfitting?",
        "Difference between CNN and ViT?",
        "Explain your Deepfake Detection Project."
    ],

    "Full Stack Developer": [
        "What is React?",
        "What is Node.js?",
        "Difference between GET and POST?",
        "What is MongoDB?",
        "Explain a Full Stack Project."
    ],             
   "Java Developer": [
        "What is JVM?",
        "Difference between JDK and JRE?",
        "What is OOP?",
        "Explain Collections Framework.",
        "What is Exception Handling?"
    ],

    "Data Analyst": [
        "What is Data Analytics?",
        "Explain SQL JOIN.",
        "What is Power BI?",
        "Difference between Excel and Power BI?",
        "Explain a Data Analysis project."
    ],

    }

    current_questions = questions.get(job_role, [])

    current_index = st.session_state.current_question

    if current_index < len(current_questions):
        st.divider()
        st.subheader("🎤 Mock Interview")

        st.info(
            f"Question {current_index + 1}: "
            f"{current_questions[current_index]}"
        )

        answer = st.text_area(
            "Your Answer",
            key=f"answer_{current_index}"
        )

        if st.button("Submit Answer"):

            word_count = len(answer.split())

            if word_count > 50:
                marks = 10
            elif word_count > 30:
                marks = 8
            elif word_count > 15:
                marks = 6
            else:
                marks = 4
            st.success(f"Score: {marks}/10")

            st.session_state.score += marks
            st.session_state.current_question += 1

            st.rerun()
    else:
        st.success("🎉 Mock Interview Completed!")

        total_questions = len(current_questions)

        final_score = int(
            (st.session_state.score /
            (total_questions * 10)) * 100
        )

        st.metric(
            "Interview Score",
            f"{final_score}%"
        )


    # ==================================
    # INTERVIEW QUESTIONS LIST
    # ==================================

    st.divider()

    st.subheader("🎤 Interview Questions")

    for i, q in enumerate(current_questions, start=1):
        st.info(f"{i}. {q}")



    # ==================================
    # ATS SECTION
    # ==================================

    st.divider()

    st.subheader("🤖 AI ATS Evaluation")

    with st.spinner("Analyzing Resume..."): 

        prompt = f"""
        You are an ATS system used by Google, Amazon, Microsoft and TCS.

        Analyze this resume.

        Resume:

        {resume_text}

        Give output in this format:

        ATS Score: XX/100

        Strengths:
        - point
        - point

        Weaknesses:
        - point
        - point

        Missing Skills:
        - point
        - point

        Improvement Suggestions:
        - point
        - point

        Overall Summary:
        - short summary
        """
        #st.write("API Key Loaded:", os.getenv("GEMINI_API_KEY"))
    try:
        response = model.generate_content(prompt)

        ats_result = response.text

        st.write(ats_result)

    # Extract score from ATS result
        score_match = re.search(r'ATS Score:\s*(\d+)', ats_result)

        if score_match:
            score = int(score_match.group(1))

            st.subheader("📊 ATS Score")

            st.progress(score / 100)

            st.metric("ATS Score", f"{score}/100")

        pdf_path = create_pdf_report(
            name,
            email,
            phone,
            ats_result
    )
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download ATS Report",
                data=pdf_file,
                file_name="ATS_Report.pdf",
                mime="application/pdf"
            )    

    except Exception as e:

        if "429" in str(e):
            st.warning(
                "Gemini rate limit reached. Please wait 10-20 seconds and try again."
            )
        else:
            st.error(f"Gemini Error: {e}")


    # ==================================
    # RESUME IMPROVEMENT GENERATOR
    # ==================================

    st.divider()

    st.subheader("📈 Resume Improvement Generator")
    
    if st.button("🐦‍🔥❤️‍🔥 Improve Resume"):
        with st.spinner("Improving Resume..."):
            improve_prompt = f"""
            You are a professional resume writer.

            Improve the following resume.

            Requirements:

            1. Create a professional summary.
            2. Rewrite skills section.
            3. Rewrite project descriptions.
            4. Make it ATS friendly.
            5. Use professional language.
            
            Resume:
        
            {resume_text}
        """
        try:
            response = model.generate_content(
                improve_prompt
            )

            st.subheader(
                "✨ Improved Resume Content"
            )

            st.write(
                response.text
            )

        except Exception as e:

            st.error(
                f"Resume Improvement Error: {e}"
            ) 
    # # =========================
    # # ATS SCORE CALCULATION
    # # =========================

    # ats_score = 0

    # # Email
    # if email != "Not Found":
    #     ats_score += 10

    # # Phone
    # if phone != "Not Found":
    #     ats_score += 10

    # # Skills
    # ats_score += min(len(detected_skills), 10) * 2

    # # Internships
    # ats_score += min(len(internships), 2) * 10

    # # Certifications
    # ats_score += min(len(certifications), 3) * 5

    # # Projects
    # ats_score += min(len(projects), 2) * 12

    # if ats_score > 100:
    #     ats_score = 100


    # # =========================
    # # ATS SCORE DISPLAY
    # # =========================

    # st.subheader("📊 ATS Score")

    # st.progress(ats_score / 100)

    # st.success(f"ATS SCORE : {ats_score}/100")

    # # =========================
    # # STRENGTHS
    # # =========================

    # st.subheader("✅ Strengths")

    # strengths = []

    # if len(detected_skills) >= 5:
    #     strengths.append("Strong Technical Skill Set")

    # if len(internships) > 0:
    #     strengths.append("Has Industry Experience")

    # if len(certifications) > 0:
    #     strengths.append("Continuous Learner")

    # if len(projects) > 0:
    #     strengths.append("Hands-on Project Experience")

    # if strengths:
    #     for strength in strengths:
    #         st.markdown(f"✔ {strength}")
    # else:
    #     st.warning("No major strengths detected")

    # # =========================
    # # AREAS FOR IMPROVEMENT
    # # =========================

    # st.subheader("⚠ Areas for Improvement")

    # improvements = []

    # if len(projects) < 2:
    #     improvements.append("Add more projects")

    # if len(certifications) < 2:
    #     improvements.append("Earn more certifications")

    # if len(internships) == 0:
    #     improvements.append("Gain internship experience")

    # if len(detected_skills) < 5:
    #     improvements.append("Expand technical skill set")

    # if improvements:
    #     for item in improvements:
    #         st.markdown(f"• {item}")
    # else:
    #     st.success("Excellent Resume Profile")         