import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import re

st.set_page_config(page_title="AI Resume Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3em;
        background-color: #0d6efd; color: white; font-weight: bold; border: none;
    }
    .header-style {
        padding: 20px; background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white; border-radius: 10px; text-align: center; margin-bottom: 25px;
    }
    .resume-card {
        background: white; padding: 40px; border: 1px solid #ddd;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: black;
    }
    .latex-header {
        color: #0000ff; border-bottom: 1.5px solid black;
        font-size: 1.1em; font-weight: bold; margin-top: 15px; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-style"><h1>🚀 AI Resume Pro</h1><p>LaTeX-Style ATS Optimizer</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🎨 Design & API")
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = st.text_input("Gemini API Key:", type="password")

col_input, col_preview = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("📝 Professional Profile")
    name = st.text_input("Full Name", placeholder="Aryan Sharma")
    email = st.text_input("Email Address", placeholder="aryan.sharma@email.com")
    
    with st.expander("🎓 Education & Certs"):
        education = st.text_area("Education", "B.Tech in Computer Science, XYZ Institute of Technology | 2022 - 2026. CGPA: 9.1/10")
        certificates = st.text_area("Certifications", "Google Cloud Digital Leader | 2025, Meta Front-End Developer | 2024")

    with st.expander("🛠️ Skills & Experience"):
        skills = st.text_area("Skills", "Python, Java, JavaScript, React, Node.js, Docker, Git")
        experience = st.text_area("Work Experience", "Web Development Intern at TechFlow Solutions (June 2025 - Aug 2025)")

    with st.expander("🚀 Projects & Achievements"):
        projects = st.text_area("Key Projects", "AI Resume Builder using Streamlit, Smart Attendance System using IoT")
        achievements = st.text_area("Top Achievements", "Finalist at Smart India Hackathon 2025, Winner of University Coding Challenge")
    
    if st.button("Generate & Optimize ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"Rewrite this for a professional resume. IMPORTANT: Use NO asterisks, NO bolding, and NO special Markdown symbols. Use only plain text. Name: {name}, Email: {email}, Education: {education}, Skills: {skills}, Experience: {experience}, Projects: {projects}, Certificates: {certificates}, Achievements: {achievements}."
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
            except Exception as e:
                st.error(f"Error: {e}")

with col_preview:
    st.subheader("🔍 LaTeX-Style Preview")
    if "resume_text" in st.session_state:
        raw_text = st.session_state.resume_text
        clean_display = raw_text.replace('*', '').replace('#', '')

        st.markdown(f"""
        <div class="resume-card">
            <h2 style="text-align:center; margin:0;">{name.upper()}</h2>
            <p style="text-align:center; font-size:0.9em; border-bottom:1px solid #eee; padding-bottom:10px;">{email} | LinkedIn | GitHub</p>
            <div class="latex-header">Professional Summary</div>
            <p style="font-size:0.9em; margin-top:5px;">{clean_display[:500]}...</p>
        </div>
        """, unsafe_allow_html=True)

        class ResumePDF(FPDF):
            def add_section(self, title, content):
                self.set_text_color(0, 0, 255)
                self.set_font("Arial", 'B', 11)
                self.cell(0, 8, title.upper(), ln=True)
                self.set_draw_color(0, 0, 0)
                self.line(10, self.get_y(), 200, self.get_y())
                self.ln(2)
                self.set_text_color(0, 0, 0)
                self.set_font("Arial", '', 10)
                # Remove Markdown artifacts
                clean_content = re.sub(r'[*#_]', '', content)
                safe_content = clean_content.encode('latin-1', 'replace').decode('latin-1')
                self.multi_cell(0, 6, safe_content)
                self.ln(3)

        pdf = ResumePDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, name.upper(), ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, f"{email} | LinkedIn | GitHub", ln=True, align='C')
        pdf.ln(5)

        pdf.add_section("Professional Summary", clean_display)
        pdf.add_section("Technical Skills", skills)
        pdf.add_section("Education", education)
        pdf.add_section("Professional Experience", experience)
        pdf.add_section("Projects", projects)
        pdf.add_section("Certifications", certificates)
        pdf.add_section("Achievements", achievements)

        st.download_button(
            label="📥 Download Structured PDF",
            data=pdf.output(dest='S').encode('latin-1'),
            file_name=f"{name}_Resume.pdf",
            mime="application/pdf"
        )
