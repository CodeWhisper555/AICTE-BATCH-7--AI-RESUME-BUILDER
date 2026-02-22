import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="AI Resume Pro", layout="wide")

st.title("AI Resume & Portfolio Builder")


with st.sidebar:
    st.header("Design & API")
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
    # Template Selection
    template_style = st.selectbox("Choose Template Style", ["Classic (Serif)", "Modern (Sans)", "Minimalist"])
    st.divider()

col_input, col_preview = st.columns([1, 1])

with col_input:
    st.subheader("Your Details")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    skills = st.text_area("Skills")
    experience = st.text_area("Experience")
    job_desc = st.text_area("Job Description")
    
    if st.button("Generate & Preview"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                
                # Using the latest stable Flash model for 2026
                
                model = genai.GenerativeModel('gemini-flash-latest')
            
                prompt = f"Create a professional resume for {name}. Email: {email}. Skills: {skills}. Experience: {experience}. Target Job: {job_desc}. Use plain text only."
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
            except Exception as e:
                st.error(f"Model Error: {e}. Try 'gemini-1.5-flash' if 2.0 is not yet active in your region.")
        else:
            st.error("Missing API Key")
with col_preview:
    st.subheader("Live Preview")
    if "resume_text" in st.session_state:
        text_to_export = st.session_state.resume_text
        
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding:20px; border-radius:10px; background-color:#f9f9f9; color:black;">
            {text_to_export.replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()

        # Prepare PDF in memory
        pdf = FPDF()
        pdf.add_page()
        
        if template_style == "Classic (Serif)":
            pdf.set_font("Times", size=12)
        elif template_style == "Modern (Sans)":
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt=name, ln=1, align='C')
            pdf.set_font("Arial", size=11)
        else:
            pdf.set_font("Courier", size=10)

        # Clean text for PDF (Removes characters that FPDF can't handle)
        clean_text = text_to_export.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_text)
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        
        st.download_button(
            label="📥 Download PDF Resume",
            data=pdf_output,
            file_name="resume.pdf",
            mime="application/pdf"
        )
