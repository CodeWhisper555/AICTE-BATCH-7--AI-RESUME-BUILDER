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
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: black;
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
    
    with st.expander("🎓 Education"):
        edu_input = st.text_area("Education Details", "B.Tech in Computer Science, XYZ Institute of Technology | 2022 - 2026. CGPA: 9.1/10")
    
    with st.expander("💼 Experience"):
        for i, exp in enumerate(st.session_state.experiences):
            exp["role"] = st.text_input(f"Role {i+1}", key=f"role_{i}")
            exp["desc"] = st.text_area(f"Description {i+1}", key=f"exp_desc_{i}")
        if st.button("➕ Add Experience"):
            st.session_state.experiences.append({})
            st.rerun()

    with st.expander("🚀 Projects"):
        for j, proj in enumerate(st.session_state.projects):
            proj["name"] = st.text_input(f"Project Name {j+1}", key=f"p_name_{j}")
            proj["desc"] = st.text_area(f"Project Description {j+1}", key=f"p_desc_{j}")
        if st.button("➕ Add Project"):
            st.session_state.projects.append({})
            st.rerun()

    if st.button("Generate AI Content ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"Write a professional resume summary and bullet points for {name}. Use no special symbols. Education: {edu_input}. Skills: {st.session_state.experiences}."
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
            except Exception as e:
                st.error(f"Error: {e}")

with col_preview:
    st.subheader("🔍 Document Preview")
    if "resume_text" in st.session_state:
        txt = st.session_state.resume_text
        clean_txt = re.sub(r'[*#_]', '', txt)

        st.markdown(f'<div class="resume-card"><div class="latex-header">Summary</div>{clean_txt[:300]}...</div>', unsafe_allow_html=True)
        
        # PDF Logic
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, name.upper(), ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, email, ln=True, align='C')
        
        # HTML Portfolio Logic
        portfolio_html = f"""
        <html><body style='background:#011f26; color:#b3b38a; font-family:sans-serif; padding:40px;'>
            <h1>{name}</h1><hr>
            <h3>Professional Summary</h3><p>{clean_txt}</p>
            <h3>Education</h3><p>{edu_input}</p>
        </body></html>
        """

        st.divider()
        st.download_button("📥 Download PDF Resume", pdf.output(dest='S').encode('latin-1'), f"{name}_Resume.pdf")
        st.download_button("🌐 Download Portfolio HTML", portfolio_html, "portfolio.html")
