import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="AI Resume Pro", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #0d6efd;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0a58ca;
    }
    .header-style {
        padding: 20px;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 25px;
    }
    .resume-card {
        background: white;
        padding: 40px;
        border: 1px solid #ddd;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: black;
    }
    .latex-header {
        color: #0000ff;
        border-bottom: 1.5px solid black;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 5px;
        text-transform: uppercase;
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
    
    st.divider()
    st.success("LaTeX Mode: Active")

col_input, col_preview = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("📝 Professional Profile")
    
    with st.expander("👤 Personal Information", expanded=True):
        name = st.text_input("Full Name", placeholder="Aryan Sharma")
        email = st.text_input("Email Address", placeholder="aryan.sharma@email.com")
        
    with st.expander("🎓 Education & Certs"):
        education = st.text_area("Education", placeholder="B.Tech in AI & ML, 9.61 CGPA")
        certificates = st.text_area("Certifications", placeholder="IBM AI Fundamentals, Cisco Python")

    with st.expander("🛠️ Skills & Experience"):
        skills = st.text_area("Skills", placeholder="Python, Java, AI-Augmented Engineering")
        experience = st.text_area("Work Experience", placeholder="Internship roles and responsibilities")

    with st.expander("🚀 Projects & Achievements"):
        projects = st.text_area("Key Projects", placeholder="Data Profiler, Smart Attendance")
        achievements = st.text_area("Top Achievements", placeholder="SIH Finalist, Coding Winner")
    
    job_desc = st.text_area("🎯 Target Job Description", height=100)
    
    if st.button("Generate & Optimize ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"Using professional action verbs and no markdown symbols, rewrite this for an ATS-optimized resume. Name: {name}, Email: {email}, Education: {education}, Skills: {skills}, Experience: {experience}, Projects: {projects}, Certificates: {certificates}, Achievements: {achievements}. Target Job: {job_desc}."
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please provide an API key.")

with col_preview:
    st.subheader("🔍 LaTeX-Style Preview")
    if "resume_text" in st.session_state:
        txt = st.session_state.resume_text
        
        st.markdown(f"""
        <div class="resume-card">
            <h1 style="text-align:center; margin-bottom:0;">{name.upper()}</h1>
            <p style="text-align:center; font-size:0.9em;">{email} | LinkedIn | GitHub | LeetCode</p>
            <div class="latex-header">Summary</div>
            <p style="font-size:0.9em;">{txt[:400]}...</p>
            <div class="latex-header">Technical Skills</div>
            <p style="font-size:0.9em;">{skills}</p>
            <div class="latex-header">Education</div>
            <p style="font-size:0.9em;">{education}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()

        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, name.upper(), ln=True, align='C')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, f"{email} | LinkedIn | GitHub | LeetCode", ln=True, align='C')
        pdf.ln(5)

        def add_latex_section(pdf, title, content):
            pdf.set_text_color(0, 0, 255)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 8, title.upper(), ln=True)
            pdf.set_draw_color(0, 0, 0)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", '', 10)
            clean_content = content.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, clean_content)
            pdf.ln(3)

        add_latex_section(pdf, "Summary", txt)
        add_latex_section(pdf, "Technical Skills", skills)
        add_latex_section(pdf, "Education", education)
        add_latex_section(pdf, "Projects", projects)
        add_latex_section(pdf, "Certifications", certificates)
        add_latex_section(pdf, "Achievements", achievements)

        pdf_output = pdf.output(dest='S').encode('latin-1')
        
        st.download_button(
            label="📥 Download LaTeX-Styled PDF",
            data=pdf_output,
            file_name=f"{name}_Resume.pdf",
            mime="application/pdf"
        )
