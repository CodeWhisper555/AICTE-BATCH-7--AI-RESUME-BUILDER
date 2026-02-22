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
        padding: 20px; background: linear-gradient(90deg, #011f26 0%, #02303a 100%);
        color: #b3b38a; border-radius: 10px; text-align: center; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-style"><h1>🤖 AI Resume & Portfolio Builder</h1><p>Professional LaTeX Style Engine</p></div>', unsafe_allow_html=True)

def clean_for_pdf(text):
    if not text: return ""
    replacements = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u20b9': 'Rs.'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.encode('latin-1', 'replace').decode('latin-1')

if "experiences" not in st.session_state: 
    st.session_state.experiences = [{"role": "", "company": "", "date": "", "desc": ""}]
if "projects" not in st.session_state: 
    st.session_state.projects = [{"name": "", "tech": "", "desc": ""}]

with st.sidebar:
    st.header("🎨 API Configuration")
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = st.text_input("Gemini API Key:", type="password")

col_input, col_preview = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("📝 Resume Data")
    name = st.text_input("Full Name", placeholder="e.g. John Doe")
    email = st.text_input("Email", placeholder="e.g. john.doe@example.com")
    phone = st.text_input("Mobile", placeholder="e.g. +91 9876543210")
    location = st.text_input("Location", placeholder="e.g. City, Country")
    
    with st.expander("🎓 Education History", expanded=True):
        edu_input = st.text_area("Education", placeholder="University Name | Degree | Grade | Years")

    with st.expander("💼 Experience"):
        for i, exp in enumerate(st.session_state.experiences):
            st.session_state.experiences[i]["role"] = st.text_input(f"Role {i+1}", value=exp.get("role", ""), key=f"role_{i}")
            st.session_state.experiences[i]["company"] = st.text_input(f"Company {i+1}", value=exp.get("company", ""), key=f"comp_{i}")
            st.session_state.experiences[i]["date"] = st.text_input(f"Duration {i+1}", value=exp.get("date", ""), key=f"dur_{i}")
            st.session_state.experiences[i]["desc"] = st.text_area(f"Bullets {i+1}", value=exp.get("desc", ""), key=f"exp_desc_{i}")
        if st.button("➕ Add Experience"):
            st.session_state.experiences.append({"role": "", "company": "", "date": "", "desc": ""})
            st.rerun()

    with st.expander("🚀 Projects"):
        for j, proj in enumerate(st.session_state.projects):
            st.session_state.projects[j]["name"] = st.text_input(f"Project Name {j+1}", value=proj.get("name", ""), key=f"p_name_{j}")
            st.session_state.projects[j]["tech"] = st.text_input(f"Technologies {j+1}", value=proj.get("tech", ""), key=f"p_tech_{j}")
            st.session_state.projects[j]["desc"] = st.text_area(f"Key Features {j+1}", value=proj.get("desc", ""), key=f"p_desc_{j}")
        if st.button("➕ Add Project"):
            st.session_state.projects.append({"name": "", "tech": "", "desc": ""})
            st.rerun()

    if st.button("Generate Professional Resume ✨"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"Professional summary and skills for {name}. Format: [SUMMARY] text [SKILLS] text."
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
                self.cell(100, 10, clean_for_pdf(name))
                self.set_font("Arial", '', 10)
                self.cell(0, 10, f"Location: {clean_for_pdf(location)}", ln=True, align='R')
                self.set_font("Arial", '', 9)
                self.cell(0, 5, "LinkedIn | GitHub | Portfolio", ln=True)
                self.cell(0, 5, f"Email: {clean_for_pdf(email)} | Mobile: {clean_for_pdf(phone)}", ln=True)
                self.ln(5)

            def add_section_title(self, title):
                self.set_font("Arial", 'B', 11)
                self.cell(0, 6, title.upper(), ln=True)
                self.line(10, self.get_y(), 200, self.get_y())
                self.ln(2)

        pdf = ProfessionalPDF()
        pdf.add_page()
        pdf.add_header()

        # PDF Sections (Summary, Skills, Education, Experience, Projects)
        sections = [("Summary", summary), ("Technical Skills", skills)]
        for title, content in sections:
            pdf.add_section_title(title)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 5, clean_for_pdf(content))
            pdf.ln(4)

        pdf.add_section_title("Education")
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, clean_for_pdf(edu_input))
        pdf.ln(4)

        pdf.add_section_title("Experience")
        for exp in st.session_state.experiences:
            if exp.get("role"):
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(120, 5, clean_for_pdf(f"{exp['role']} - {exp['company']}"))
                pdf.cell(0, 5, clean_for_pdf(exp['date']), ln=True, align='R')
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 5, f"- {clean_for_pdf(exp['desc'])}")
                pdf.ln(2)

        # Portfolio HTML Generation
        portfolio_html = f"""
        <html><body style='background:#011f26; color:#b3b38a; font-family:sans-serif; padding:50px;'>
            <h1>{name}</h1><p>{location} | {email}</p><hr>
            <h2>Summary</h2><p>{summary}</p>
            <h2>Projects</h2><ul>{"".join([f"<li>{p['name']}: {p['desc']}</li>" for p in st.session_state.projects if p.get('name')])}</ul>
        </body></html>
        """

        st.download_button("📥 Download Final PDF", pdf.output(dest='S'), f"Resume.pdf")
        st.download_button("🌐 Download Portfolio HTML", portfolio_html, "portfolio.html")
