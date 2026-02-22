"""
views/builder.py — Comprehensive Resume Builder
================================================
Collects all resume data from the user with a step-by-step form.
AI enhances each section using Gemini.
Generates a downloadable PDF.
"""

import streamlit as st
from utils.gemini_client import generate
from utils.pdf_generator import build_pdf, TEMPLATES


def show():
    st.markdown(
        """
        <h1 style='color:#6C63FF;'>📝 Resume Builder</h1>
        <p style='color:gray;'>Fill in your details step by step. Use the AI Enhance buttons to make each section shine.</p>
        <hr/>
        """,
        unsafe_allow_html=True,
    )

    # ── Progress Tracker ──────────────────────────────────────────────────────
    steps = ["Personal Info", "Education", "Experience", "Projects", "Skills", "Extras", "Generate"]
    progress_html = "<div style='display:flex; gap:8px; margin-bottom:20px; flex-wrap:wrap;'>"
    for i, s in enumerate(steps):
        color = "#6C63FF" if i == 0 else "#ddd"
        progress_html += f"<span style='background:{color}; color:{'white' if i==0 else '#999'}; padding:4px 12px; border-radius:20px; font-size:0.8rem;'>{s}</span>"
    progress_html += "</div>"
    st.markdown(progress_html, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 1 — Personal Info
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("👤 Step 1 — Personal Information", expanded=True):
        st.markdown("*These details appear at the top of your resume.*")
        c1, c2 = st.columns(2)
        with c1:
            name      = st.text_input("Full Name *", placeholder="Priya Sharma")
            email     = st.text_input("Email Address *", placeholder="priya@gmail.com")
            phone     = st.text_input("Phone Number *", placeholder="+91 9876543210")
        with c2:
            location  = st.text_input("City, State *", placeholder="Hyderabad, Telangana")
            linkedin  = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/priyasharma")
            github    = st.text_input("GitHub URL", placeholder="github.com/priyasharma")
        target_role   = st.text_input("🎯 Target Job Role / Internship *", placeholder="Data Science Intern / Software Developer")

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 2 — Professional Summary
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("🗒️ Step 2 — Professional Summary", expanded=False):
        st.markdown("*2-3 sentences about who you are and what you bring. AI will polish it.*")
        summary = st.text_area(
            "Write your summary (or leave rough notes — AI will fix it)",
            placeholder="Final year B.Tech CSE student with interests in data science and ML. Built 3 projects using Python and TensorFlow. Looking for a data science internship.",
            height=100,
            key="summary_input",
        )
        if st.button("🤖 Enhance Summary with AI", key="enhance_summary"):
            if summary and target_role:
                prompt = f"""
You are a professional resume writer for students and freshers.
Rewrite this summary for a student applying for: {target_role}

Original: {summary}

Requirements:
- 2-3 impactful sentences
- Use strong action-oriented language
- Mention the role they're targeting
- Sound enthusiastic but professional
- No filler phrases like "passionate about" or "highly motivated"
- Return ONLY the improved summary, nothing else.
"""
                improved = generate(prompt, "✨ Enhancing your summary...")
                st.session_state["summary_enhanced"] = improved
            else:
                st.warning("Please fill in your summary and target role first.")

        if "summary_enhanced" in st.session_state:
            st.success("✅ AI-Enhanced Summary:")
            st.text_area("", value=st.session_state["summary_enhanced"], height=90, key="summary_display")
            st.caption("Copy the above and paste it as your final summary.")

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 3 — Education
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("🎓 Step 3 — Education", expanded=False):
        st.markdown("*Add your most recent degree first. Include 10th & 12th if fresher.*")
        num_edu = st.number_input("Number of education entries", 1, 4, 2, key="num_edu")
        education = []
        for i in range(int(num_edu)):
            st.markdown(f"**📚 Education {i+1}**")
            ec1, ec2, ec3, ec4 = st.columns([3, 3, 2, 2])
            with ec1: degree = st.text_input("Degree / Board", key=f"degree_{i}", placeholder="B.Tech CSE / Class 12")
            with ec2: institution = st.text_input("College / School", key=f"institution_{i}", placeholder="JNTU Hyderabad")
            with ec3: year = st.text_input("Year", key=f"year_{i}", placeholder="2020 – 2024")
            with ec4: grade = st.text_input("CGPA / %", key=f"grade_{i}", placeholder="8.5 / 10")
            education.append({"degree": degree, "institution": institution, "year": year, "grade": grade})
            if i < int(num_edu) - 1:
                st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 4 — Internships & Experience
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("💼 Step 4 — Internships & Work Experience", expanded=False):
        st.markdown("*Include internships, part-time jobs, freelance work. Freshers can skip if none.*")
        num_exp = st.number_input("Number of experience entries (0 if none)", 0, 5, 1, key="num_exp")
        experiences = []
        for i in range(int(num_exp)):
            st.markdown(f"**🏢 Experience {i+1}**")
            xc1, xc2, xc3 = st.columns([3, 3, 2])
            with xc1: exp_role = st.text_input("Role / Designation", key=f"exp_role_{i}", placeholder="Data Science Intern")
            with xc2: exp_company = st.text_input("Company / Organization", key=f"exp_company_{i}", placeholder="TCS / StartupXYZ")
            with xc3: exp_dur = st.text_input("Duration", key=f"exp_dur_{i}", placeholder="May 2023 – Jul 2023")
            exp_desc = st.text_area(
                "What did you do? (bullet points preferred)",
                key=f"exp_desc_{i}",
                placeholder="• Built a sentiment analysis model with 87% accuracy using LSTM\n• Automated report generation saving 5 hours per week\n• Collaborated with a team of 4 engineers",
                height=100,
            )
            if st.button(f"🤖 Enhance Experience {i+1} with AI", key=f"enhance_exp_{i}"):
                if exp_desc:
                    prompt = f"""
Improve this internship/work experience description for a student's resume.
Role: {exp_role} at {exp_company}
Target Job: {target_role if 'target_role' in dir() else 'Software/Data role'}

Original:
{exp_desc}

Rules:
- Use bullet points starting with strong action verbs (Built, Developed, Designed, Improved, etc.)
- Add quantifiable impact wherever possible
- Keep it under 4 bullet points
- Return ONLY the improved bullet points.
"""
                    improved_exp = generate(prompt, f"✨ Enhancing experience {i+1}...")
                    st.session_state[f"exp_enhanced_{i}"] = improved_exp
                else:
                    st.warning("Please enter description first.")

            if f"exp_enhanced_{i}" in st.session_state:
                st.success(f"✅ Enhanced Experience {i+1}:")
                st.text_area("", value=st.session_state[f"exp_enhanced_{i}"], height=100, key=f"exp_display_{i}")

            experiences.append({"role": exp_role, "company": exp_company, "duration": exp_dur, "description": exp_desc})
            if i < int(num_exp) - 1:
                st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 5 — Projects
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("🛠️ Step 5 — Projects", expanded=False):
        st.markdown("*Your projects are your portfolio! List 2-4 strong ones with tech stack.*")
        num_proj = st.number_input("Number of projects", 1, 6, 2, key="num_proj")
        all_projects = []
        for i in range(int(num_proj)):
            st.markdown(f"**💡 Project {i+1}**")
            pc1, pc2 = st.columns(2)
            with pc1: proj_name = st.text_input("Project Name", key=f"proj_name_{i}", placeholder="Fake News Detector")
            with pc2: proj_tech = st.text_input("Technologies Used", key=f"proj_tech_{i}", placeholder="Python, NLP, LSTM, Flask")
            proj_link = st.text_input("GitHub / Live Link (optional)", key=f"proj_link_{i}", placeholder="github.com/priya/fake-news")
            proj_desc = st.text_area(
                "Project Description",
                key=f"proj_desc_{i}",
                placeholder="Built a machine learning model to classify news articles as real or fake with 94% accuracy.",
                height=80,
            )
            if st.button(f"🤖 Enhance Project {i+1} with AI", key=f"enhance_proj_{i}"):
                if proj_desc:
                    prompt = f"""
Improve this project description for a student resume.
Project: {proj_name} | Tech: {proj_tech}

Original: {proj_desc}

Rules:
- Start with an action verb
- Mention the tech stack naturally
- Include the impact/outcome (accuracy, users, speed improvement etc.)
- 1-2 concise sentences max
- Return ONLY the improved description.
"""
                    improved_proj = generate(prompt, f"✨ Enhancing project {i+1}...")
                    st.session_state[f"proj_enhanced_{i}"] = improved_proj

            if f"proj_enhanced_{i}" in st.session_state:
                st.success(f"✅ Enhanced Project {i+1}:")
                st.text_area("", value=st.session_state[f"proj_enhanced_{i}"], height=70, key=f"proj_display_{i}")

            link_text = f" | {proj_link}" if proj_link else ""
            all_projects.append(f"• {proj_name} ({proj_tech}){link_text}: {proj_desc}")
            if i < int(num_proj) - 1:
                st.markdown("---")

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 6 — Skills
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("⚡ Step 6 — Technical Skills", expanded=False):
        st.markdown("*Be specific. Group by category for better readability.*")
        c1, c2 = st.columns(2)
        with c1:
            prog_langs = st.text_input("Programming Languages", placeholder="Python, Java, C++, JavaScript")
            frameworks = st.text_input("Frameworks & Libraries", placeholder="TensorFlow, React, Django, Flask")
            databases  = st.text_input("Databases", placeholder="MySQL, MongoDB, PostgreSQL")
        with c2:
            tools      = st.text_input("Tools & Platforms", placeholder="Git, Docker, VS Code, Jupyter")
            cloud      = st.text_input("Cloud / DevOps (if any)", placeholder="AWS, GCP, GitHub Actions")
            soft_skills = st.text_input("Soft Skills", placeholder="Team Player, Problem Solving, Communication")

        skills_combined = []
        if prog_langs:  skills_combined.append(f"Languages: {prog_langs}")
        if frameworks:  skills_combined.append(f"Frameworks: {frameworks}")
        if databases:   skills_combined.append(f"Databases: {databases}")
        if tools:       skills_combined.append(f"Tools: {tools}")
        if cloud:       skills_combined.append(f"Cloud/DevOps: {cloud}")
        if soft_skills: skills_combined.append(f"Soft Skills: {soft_skills}")
        skills_text = "\n".join(skills_combined)

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 7 — Achievements & Extras
    # ════════════════════════════════════════════════════════════════════════
    with st.expander("🏆 Step 7 — Achievements, Certifications & Extra-Curriculars", expanded=False):
        achievements = st.text_area(
            "Achievements & Certifications",
            placeholder="• Google Data Analytics Certificate – Coursera (2023)\n• Ranked Top 5% in HackerRank Python Assessment\n• Won 1st place in College Hackathon (2023)",
            height=90,
        )
        extra = st.text_area(
            "Extra-Curricular Activities",
            placeholder="• NSS Volunteer – Organized blood donation camp for 200+ participants\n• Technical Lead, College Coding Club (2022-23)",
            height=80,
        )

    # ════════════════════════════════════════════════════════════════════════
    # SECTION 8 — Template Selection & PDF Generation
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.subheader("🎨 Step 8 — Choose Template & Generate PDF")

    template_name = st.selectbox(
        "Select Resume Template",
        list(TEMPLATES.keys()),
        help="All templates are ATS-friendly. Choose based on your industry.",
    )

    template_descriptions = {
        "🎯 Classic Professional": "Best for: Government jobs, banking, traditional companies",
        "💜 Modern Purple": "Best for: Tech companies, startups, product roles",
        "🌊 Corporate Blue": "Best for: Consulting, engineering, MBA programs",
        "🍃 Minimal Green": "Best for: Healthcare, education, NGOs",
        "🔥 Bold Red": "Best for: Marketing, sales, creative roles",
    }
    st.info(f"💡 {template_descriptions.get(template_name, '')}")

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.button("🚀 Generate My Resume PDF", use_container_width=True, type="primary"):
        # Validation
        required = {"Full Name": name, "Email": email, "Phone": phone, "Location": location, "Target Role": target_role}
        missing = [k for k, v in required.items() if not v.strip()]
        if missing:
            st.error(f"⚠️ Please fill in: {', '.join(missing)}")
        else:
            # Use AI-enhanced versions if available
            final_summary = st.session_state.get("summary_enhanced", summary)
            final_projects = "\n".join(
                st.session_state.get(f"proj_enhanced_{i}", all_projects[i] if i < len(all_projects) else "")
                for i in range(int(num_proj))
            )

            resume_data = {
                "name": name, "email": email, "phone": phone,
                "location": location, "linkedin": linkedin, "github": github,
                "summary": final_summary,
                "education": education,
                "experience": experiences,
                "projects": final_projects or "\n".join(all_projects),
                "skills": skills_text,
                "achievements": achievements,
                "extra": extra,
            }

            with st.spinner("📄 Building your resume PDF..."):
                pdf_bytes = build_pdf(resume_data, template_name)

            st.success("🎉 Your resume is ready!")
            st.balloons()

            st.download_button(
                label=f"⬇️ Download Resume PDF",
                data=pdf_bytes,
                file_name=f"{name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

            st.markdown(
                """
                <div style='background:#f0eeff; border-radius:10px; padding:16px; margin-top:12px;'>
                    <b>✅ Next Steps:</b><br/>
                    🎯 Go to <b>ATS Score Checker</b> to test your resume against a job description<br/>
                    ✉️ Go to <b>Cover Letter Generator</b> to complete your application<br/>
                    💡 Go to <b>LinkedIn Summary</b> to update your profile
                </div>
                """,
                unsafe_allow_html=True,
            )
