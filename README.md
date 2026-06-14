# 🚀 AI Recruitment System

An intelligent, AI-powered recruitment platform that parses resumes, calculates ATS scores, performs job role matching, and conducts mock interviews with live scoring. Powered by Streamlit and Gemini 2.5 Flash.

## ✨ Features

- **📄 Resume Parser**: Upload a PDF resume to extract key details like candidate name, email, phone, detected skills, certifications, and internships.
- **🎯 Job Role Matching**: Match candidates against roles (Python Developer, Java Developer, Data Analyst, Machine Learning Engineer, Full Stack Developer) with match percentage and gap analysis.
- **🤖 AI ATS Evaluation**: Deep resume analysis comparing against standards of top tech firms (Google, Amazon, Microsoft, TCS) with full strengths/weaknesses breakdown and downloadable PDF reports.
- **🎤 Mock Interview Simulator**: Dynamic mock interviews with role-specific questions and instant AI-based grading of answers.
- **📈 Resume Improver**: Real-time generative rewriting of resume components to make them ATS-friendly.

---

## 🛠️ Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SARVESH3226/AI-Recruitment-System.git
   cd AI-Recruitment-System
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the App:**
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Deployment to Streamlit Community Cloud

The easiest way to deploy this application for free is via **Streamlit Community Cloud**:

1. Push your repository to GitHub (this has already been pushed to `SARVESH3226/AI-Recruitment-System`).
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in using your GitHub account.
3. Click on the **New app** button.
4. Select the repository `SARVESH3226/AI-Recruitment-System`.
5. Set **Main file path** to `app.py`.
6. Open **Advanced settings** (or do this after creation under settings) and add your Secrets:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key"
   ```
7. Click **Deploy**. Your app will be live in a couple of minutes!
