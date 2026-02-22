import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="AI Resume Pro", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border: none;
    }
    .header-style {
        padding: 20px;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-style"><h1>🚀 AI Resume & Portfolio Builder</h1><p>Crafting Professional Futures with Gemini AI</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Design & API")
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = st.text_input("Gemini API Key:", type="password")
    
    template_style = st.select_slider("Select Design Density", options=["Minimalist", "Classic (Serif)", "Modern (Sans)"])
    st.divider()
    st.info("Tip: Use the 'Modern' style for Tech roles and 'Classic' for Corporate roles.")

col_input, col_preview = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("📝 Professional Profile")
    
    with st.expander("👤 Personal Information", expanded=True):
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email Address", placeholder="john@example.com")
        
    with st.expander("🎓 Education & Certifications"):
        education = st.text_area("Education", placeholder="B.Tech in CS, GPA 3.8")
        certificates = st.text_area("Certifications", placeholder="AWS Cloud Practitioner, IBM AI Engineering")

    with st.expander("🛠️ Skills & Experience"):
        skills = st.text_area("Skills", placeholder="Python, SQL, Project Management")
        experience = st.text_area("Work Experience", placeholder="Briefly describe your roles")

    with st.expander("🚀 Projects & Achievements"):
        projects = st.text_area("Key Projects", placeholder="Link or describe your best work")
        achievements = st.text_area("Top Achievements", placeholder="Awards, Competitions, etc.")
    
    job_desc = st.text_area("🎯 Target Job Description", height=150)
    
    if st.button("Generate Resume ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"Create a professional, ATS-optimized resume for {name}. Email: {email}. Education: {education}. Skills: {skills}. Experience: {experience}. Projects: {projects}. Certifications: {certificates}. Achievements: {achievements}. Target Job: {job_desc}. Use professional action verbs. Use plain text only."
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please add your API Key to proceed.")

with col_preview:
    st.subheader("🔍 Live Preview")
    if "resume_text" in st.session_state:
        text_to_export = st.session_state.resume_text
        
        st.markdown(f"""
        <div style="border:2px solid #007bff; padding:30px; border-radius:15px; background-color:white; color:#333; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); min-height: 600px;">
            {text_to_export.replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()

        pdf = FPDF()
        pdf.add_page()
        
        if template_style == "Classic (Serif)":
            pdf.set_font("Times", size=11)
        elif template_style == "Modern (Sans)":
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt=name.upper(), ln=1, align='C')
            pdf.set_font("Arial", size=10)
        else:
            pdf.set_font("Courier", size=9)

        clean_text = text_to_export.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, clean_text)
        pdf_output = pdf.output(dest='S').encode('latin-1')
        
        st.download_button(
            label="📥 Download Professional PDF",
            data=pdf_output,
            file_name=f"{name}_Resume.pdf",
            mime="application/pdf"
        )
