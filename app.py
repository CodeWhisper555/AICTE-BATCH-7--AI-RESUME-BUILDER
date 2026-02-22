import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import re

st.set_page_config(page_title="AI Resume Pro", layout="wide")

# Custom CSS for the Dashboard
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
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-style"><h1>🤖 AI Resume & Portfolio Builder</h1><p>Sai Ajay Template Engine Active</p></div>', unsafe_allow_html=True)

# Initialization of dynamic lists
if "experiences" not in st.session_state: st.session_state.experiences = [{"role": "", "company": "", "date": "", "desc": ""}]
if "projects" not in st.session_state: st.session_state.projects = [{"name": "", "tech": "", "desc": ""}]

with st.sidebar:
    st.header("🎨 API Configuration")
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = st.text_input("Gemini API Key:", type="password")

col_input, col_preview = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("📝 Resume Data")
    name = st.text_input("Full Name", value="Sai Ajay Chandra Ravuri")
    email = st.text_input("Email", value="sai.ajay.chandra.555@gmail.com")
    phone = st.text_input("Mobile", value="8712270493")
    location = st.text_input("Location", value="Vijayawada, India")
    
    with st.expander("🎓 Education History", expanded=True):
        edu_input = st.text_area("Education (One per line)", "P.V.P. Siddhartha Institute of Technology | B.Tech AI & ML | 9.61 CGPA | 2024 - 2028\nSarada Educational Institutions | Intermediate | 94% | 2022 - 2024")

    with st.expander("💼 Experience"):
        for i, exp in enumerate(st.session_state.experiences):
            st.session_state.experiences[i]["role"] = st.text_input(f"Role {i+1}", value=exp["role"], key=f"role_{i}")
            st.session_state.experiences[i]["company"] = st.text_input(f"Company {i+1}", value=exp["company"], key=f"comp_{i}")
            st.session_state.experiences[i]["date"] = st.text_input(f"Duration {i+1}", value=exp["date"], key=f"dur_{i}")
            st.session_state.experiences[i]["desc"] = st.text_area(f"Bullets {i+1}", value=exp["desc"], key=f"exp_desc_{i}")
        if st.button("➕ Add Experience"):
            st.session_state.experiences.append({"role": "", "company": "", "date": "", "desc": ""})
            st.rerun()

    if st.button("Generate Professional Resume ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"Create a professional summary and technical skills list for {name} ({edu_input}). Use no symbols. Sections: [SUMMARY], [SKILLS]."
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
            except Exception as e: st.error(f"Error: {e}")

with col_preview:
    st.subheader("🔍 Layout Preview")
    if "resume_text" in st.session_state:
        res_text = st.session_state.resume_text
        
        def get_section(header, text):
            pattern = rf"\[{header}\](.*?)(?=\[|$)"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""

        summary = get_section("SUMMARY", res_text)
        skills = get_section("SKILLS", res_text)

        class ProfessionalPDF(FPDF):
            def add_header(self):
                self.set_font("Arial", 'B', 16)
                self.cell(100, 10, name)
                self.set_font("Arial", '', 10)
                self.cell(0, 10, f"Location: {location}", ln=True, align='R')
                self.cell(0, 5, f"LinkedIn | GitHub | Leetcode", ln=True)
                self.cell(0, 5, f"Email: {email} | Mobile: {phone}", ln=True)
                self.ln(5)

            def add_section_title(self, title):
                self.set_text_color(0, 0, 0)
                self.set_font("Arial", 'B', 11)
                self.cell(0, 6, title.upper(), ln=True)
                self.line(10, self.get_y(), 200, self.get_y())
                self.ln(2)

        pdf = ProfessionalPDF()
        pdf.add_page()
        pdf.add_header()

        # Summary Section
        pdf.add_section_title("Summary")
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, summary.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(4)

        # Skills Section (Bold Labels)
        pdf.add_section_title("Technical Skills")
        for line in skills.split('\n'):
            if ":" in line:
                label, val = line.split(":", 1)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(40, 5, label.strip() + " : ")
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, val.strip())
        pdf.ln(4)

        # Education Section (Split columns)
        pdf.add_section_title("Education")
        for line in edu_input.split('\n'):
            if "|" in line:
                parts = line.split("|")
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(120, 5, parts[0].strip())
                pdf.set_font("Arial", '', 10)
                pdf.cell(0, 5, location, ln=True, align='R')
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(120, 5, parts[1].strip())
                pdf.set_font("Arial", '', 10)
                pdf.cell(0, 5, parts[3].strip() if len(parts)>3 else "", ln=True, align='R')
                pdf.ln(2)

        # Experience Section
        pdf.add_section_title("Experience")
        for exp in st.session_state.experiences:
            if exp["role"]:
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(120, 5, exp["role"])
                pdf.set_font("Arial", '', 10)
                pdf.cell(0, 5, exp["date"], ln=True, align='R')
                pdf.multi_cell(0, 5, f"• {exp['desc']}")
                pdf.ln(2)

        st.download_button("📥 Download Final PDF", pdf.output(dest='S').encode('latin-1'), f"{name}_Resume.pdf")
        st.success("Layout generated with exact template specs!")
