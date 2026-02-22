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
        background: white; padding: 40px; border: 1px solid #ddd;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: black; font-family: 'Arial';
    }
    .latex-header {
        color: #0000ff; border-bottom: 1.5px solid black;
        font-size: 1.1em; font-weight: bold; margin-top: 15px; text-transform: uppercase;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-style"><h1>🤖 AI Resume & Portfolio Builder</h1><p>Professional LaTeX Style PDF & Portfolio</p></div>', unsafe_allow_html=True)

if "experiences" not in st.session_state: st.session_state.experiences = [{"role": "", "date": "", "desc": ""}]
if "projects" not in st.session_state: st.session_state.projects = [{"name": "", "tech": "", "desc": ""}]

with st.sidebar:
    st.header("🎨 API Configuration")
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = st.text_input("Gemini API Key:", type="password")

col_input, col_preview = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("📝 User Details")
    name = st.text_input("Full Name", value="Aryan Sharma")
    email = st.text_input("Email", value="aryan.sharma@email.com")
    location = st.text_input("Location", value="Vijayawada, India")
    
    with st.expander("🎓 Education", expanded=True):
        edu_input = st.text_area("Education Details", "B.Tech in Computer Science, XYZ Institute of Technology | 2022 - 2026. CGPA: 9.1/10")
    
    with st.expander("💼 Experience"):
        for i, exp in enumerate(st.session_state.experiences):
            st.session_state.experiences[i]["role"] = st.text_input(f"Role/Company {i+1}", value=exp["role"], key=f"role_{i}")
            st.session_state.experiences[i]["date"] = st.text_input(f"Duration {i+1}", value=exp["date"], placeholder="June 2025 - Aug 2025", key=f"dur_{i}")
            st.session_state.experiences[i]["desc"] = st.text_area(f"Responsibilities {i+1}", value=exp["desc"], key=f"exp_desc_{i}")
        if st.button("➕ Add Experience"):
            st.session_state.experiences.append({"role": "", "date": "", "desc": ""})
            st.rerun()

    with st.expander("🚀 Projects"):
        for j, proj in enumerate(st.session_state.projects):
            st.session_state.projects[j]["name"] = st.text_input(f"Project Name {j+1}", value=proj["name"], key=f"p_name_{j}")
            st.session_state.projects[j]["tech"] = st.text_input(f"Technologies {j+1}", value=proj["tech"], placeholder="Python, Streamlit", key=f"p_tech_{j}")
            st.session_state.projects[j]["desc"] = st.text_area(f"Key Features {j+1}", value=proj["desc"], key=f"p_desc_{j}")
        if st.button("➕ Add Project"):
            st.session_state.projects.append({"name": "", "tech": "", "desc": ""})
            st.rerun()

    if st.button("Generate & Format Resume ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"""
                Create a professional resume for {name}. 
                Format the response with these headers: [SUMMARY], [SKILLS], [EXPERIENCE_SECTION], [PROJECT_SECTION].
                Under [EXPERIENCE_SECTION] and [PROJECT_SECTION], provide only the descriptive bullet points.
                DO NOT use bolding or asterisks.
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
        res_text = st.session_state.resume_text
        
        # Robust Parsing Logic
        def get_section(header, text):
            pattern = rf"\[{header}\](.*?)(?=\[|$)"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else "Content generating..."

        summary = get_section("SUMMARY", res_text)
        skills = get_section("SKILLS", res_text)
        exp_ai = get_section("EXPERIENCE_SECTION", res_text)
        proj_ai = get_section("PROJECT_SECTION", res_text)

        st.markdown(f"""
        <div class="resume-card">
            <h1 style="text-align:center; margin:0;">{name.upper()}</h1>
            <p style="text-align:center;">{location} | {email}</p>
            <div class="latex-header">Summary</div>
            <p style="font-size:0.9em;">{summary}</p>
            <div class="latex-header">Technical Skills</div>
            <p style="font-size:0.9em;">{skills}</p>
            <div class="latex-header">Experience</div>
            <p style="font-size:0.9em;"><b>{st.session_state.experiences[0]['role']}</b><br>{exp_ai}</p>
        </div>
        """, unsafe_allow_html=True)

        class LaTeXPDF(FPDF):
            def section_title(self, label):
                self.set_text_color(0, 0, 255)
                self.set_font("Arial", 'B', 12)
                self.cell(0, 10, label.upper(), ln=True)
                self.set_draw_color(0, 0, 0)
                self.line(10, self.get_y(), 200, self.get_y())
                self.ln(2)
                self.set_text_color(0, 0, 0)

        pdf = LaTeXPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 10, name.upper(), ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, f"{location} | {email}", ln=True, align='C')
        pdf.ln(5)

        # Summary
        pdf.section_title("Summary")
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, summary.encode('latin-1', 'replace').decode('latin-1'))
        
        # Education
        pdf.section_title("Education")
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 5, edu_input.encode('latin-1', 'replace').decode('latin-1'))

        # Experience
        pdf.section_title("Experience")
        for exp in st.session_state.experiences:
            if exp["role"]:
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(100, 5, exp["role"])
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 5, exp["date"], ln=True, align='R')
                pdf.set_font("Arial", '', 10)
                # Filter to only show bullet points from AI
                pdf.multi_cell(0, 5, exp_ai.encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(2)

        st.divider()
        st.download_button("📥 Download PDF", pdf.output(dest='S').encode('latin-1'), f"{name}_Resume.pdf")
