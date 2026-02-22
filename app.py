import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import re

st.set_page_config(page_title="AI Resume & Portfolio Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3em;
        background-color: #0d6efd; color: white; font-weight: bold; border: none;
    }
    .header-style {
        padding: 20px; background: linear-gradient(90deg, #011f26 0%, #02303a 100%);
        color: #b3b38a; border-radius: 10px; text-align: center; margin-bottom: 25px;
    }
    .resume-card {
        background: white; padding: 30px; border: 1px solid #ddd;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: black; font-family: 'Arial';
    }
    .latex-header {
        color: #0000ff; border-bottom: 1.5px solid black;
        font-size: 1.1em; font-weight: bold; margin-top: 15px; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-style"><h1>🤖 AI Resume & Portfolio Builder</h1><p>Professional LaTeX Resumes & HTML Portfolios</p></div>', unsafe_allow_html=True)

if "experiences" not in st.session_state: st.session_state.experiences = [{}]
if "projects" not in st.session_state: st.session_state.projects = [{}]

with st.sidebar:
    st.header("🎨 API Configuration")
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = st.text_input("Gemini API Key:", type="password")

col_input, col_preview = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("📝 User Details")
    name = st.text_input("Full Name", placeholder="Aryan Sharma")
    email = st.text_input("Email", placeholder="aryan.sharma@email.com")
    location = st.text_input("Location", placeholder="Vijayawada, India")
    
    with st.expander("🎓 Education"):
        edu_input = st.text_area("Education Details", "B.Tech in Computer Science, XYZ Institute of Technology | 2022 - 2026. CGPA: 9.1/10")
    
    with st.expander("💼 Experience"):
        for i, exp in enumerate(st.session_state.experiences):
            exp["role"] = st.text_input(f"Role/Company {i+1}", key=f"role_{i}")
            exp["date"] = st.text_input(f"Duration {i+1}", placeholder="June 2025 - Aug 2025", key=f"dur_{i}")
            exp["desc"] = st.text_area(f"Responsibilities {i+1}", key=f"exp_desc_{i}")
        if st.button("➕ Add Experience"):
            st.session_state.experiences.append({})
            st.rerun()

    with st.expander("🚀 Projects"):
        for j, proj in enumerate(st.session_state.projects):
            proj["name"] = st.text_input(f"Project Name {j+1}", key=f"p_name_{j}")
            proj["tech"] = st.text_input(f"Technologies {j+1}", placeholder="Python, Streamlit", key=f"p_tech_{j}")
            proj["desc"] = st.text_area(f"Key Features {j+1}", key=f"p_desc_{j}")
        if st.button("➕ Add Project"):
            st.session_state.projects.append({})
            st.rerun()

    if st.button("Generate Professional Resume ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"""
                Act as a Professional Resume Architect. Using the data provided, create highly impactful bullet points for a resume.
                Focus on strong action verbs and technical results.
                
                Format your response exactly as follows:
                SUMMARY: [One professional paragraph]
                SKILLS: [Comma separated list]
                EXPERIENCE_POINTS: [Bullet points for experiences provided]
                PROJECT_POINTS: [Bullet points for projects provided]
                
                Data:
                Name: {name}, Education: {edu_input}, Experience: {st.session_state.experiences}, Projects: {st.session_state.projects}
                """
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
            except Exception as e:
                st.error(f"Error: {e}")

with col_preview:
    st.subheader("🔍 Professional Preview")
    if "resume_text" in st.session_state:
        # Extract sections using simple string splits
        res_text = st.session_state.resume_text
        summary = res_text.split("SUMMARY:")[1].split("SKILLS:")[0].strip() if "SUMMARY:" in res_text else ""
        skills_list = res_text.split("SKILLS:")[1].split("EXPERIENCE_POINTS:")[0].strip() if "SKILLS:" in res_text else ""
        
        st.markdown(f"""
        <div class="resume-card">
            <h1 style="text-align:center; margin:0;">{name.upper()}</h1>
            <p style="text-align:center; font-size:0.9em;">{location} | {email}</p>
            <div class="latex-header">Summary</div>
            <p style="font-size:0.9em;">{summary}</p>
            <div class="latex-header">Technical Skills</div>
            <p style="font-size:0.9em;">{skills_list}</p>
            <div class="latex-header">Education</div>
            <p style="font-size:0.9em;">{edu_input}</p>
        </div>
        """, unsafe_allow_html=True)

        class LaTeXPDF(FPDF):
            def add_resume_section(self, title):
                self.set_text_color(0, 0, 255)
                self.set_font("Arial", 'B', 12)
                self.cell(0, 10, title.upper(), ln=True)
                self.set_draw_color(0, 0, 0)
                self.line(10, self.get_y(), 200, self.get_y())
                self.ln(2)
                self.set_text_color(0, 0, 0)

        pdf = LaTeXPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 10, name.upper(), ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, f"{location} | {email} | LinkedIn | GitHub", ln=True, align='C')
        pdf.ln(5)

        # Summary Section
        pdf.add_resume_section("Summary")
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, summary.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(2)

        # Education Section
        pdf.add_resume_section("Education")
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 5, edu_input.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(2)

        # Experience Section
        pdf.add_resume_section("Experience")
        for exp in st.session_state.experiences:
            if exp.get("role"):
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(100, 5, exp["role"])
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 5, exp.get("date", ""), ln=True, align='R')
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, exp.get("desc", "").replace("*", "-"))
                pdf.ln(2)

        # Projects Section
        pdf.add_resume_section("Projects")
        for proj in st.session_state.projects:
            if proj.get("name"):
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(100, 5, proj["name"])
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 5, proj.get("tech", ""), ln=True, align='R')
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, proj.get("desc", "").replace("*", "-"))
                pdf.ln(2)

        st.divider()
        st.download_button("📥 Download LaTeX-Styled PDF", pdf.output(dest='S').encode('latin-1'), f"{name}_Resume.pdf")
