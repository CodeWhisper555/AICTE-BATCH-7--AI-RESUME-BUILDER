"""
views/guide.py — How It Works / Fresher Resume Guide
"""
import streamlit as st


def show():
    st.markdown(
        """
        <h1 style='color:#6C63FF;'>📖 Fresher's Resume Guide</h1>
        <p style='color:gray;'>
            Everything a student needs to know about building a job-winning resume.
        </p>
        <hr/>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## 🗺️ How to Use SmartResumeAI")
    steps = [
        ("📝 Build My Resume", "Start here. Fill in your personal info, education, projects, skills. Use the AI Enhance buttons for each section."),
        ("🎨 Resume Templates", "Browse 5 templates and download a sample to see how yours will look before generating."),
        ("🎯 ATS Score Checker", "Paste your resume + any job description to get a match score and fix suggestions."),
        ("✉️ Cover Letter", "Generate a personalized cover letter. Do this for every unique job application."),
        ("💡 LinkedIn Summary", "Update your LinkedIn profile with an AI-generated About section to attract recruiter messages."),
    ]
    for icon_title, desc in steps:
        st.markdown(
            f"""
            <div style='
                background:#f8f7ff; border-left:4px solid #6C63FF;
                border-radius:8px; padding:14px 18px; margin-bottom:12px;
            '>
                <b style='color:#6C63FF;'>{icon_title}</b><br/>
                <span style='color:#444;'>{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("## ✅ Resume Checklist for Freshers")

    checklist_items = {
        "📋 Basic Info": [
            "Full name, phone, professional email (avoid nicknames)",
            "LinkedIn URL + GitHub URL if you have projects",
            "City and state (no full address needed)",
        ],
        "🗒️ Summary": [
            "2-3 sentences max",
            "Mentions your degree, skills, and what you're looking for",
            "Sounds confident, not desperate",
        ],
        "🎓 Education": [
            "Listed in reverse chronological order (most recent first)",
            "Includes CGPA/percentage if above 7.0/70%",
            "Include Class 10 & 12 for freshers",
        ],
        "🛠️ Projects": [
            "At least 2-3 projects with tech stack mentioned",
            "Each has a 1-2 sentence description with outcome/impact",
            "GitHub links included where possible",
        ],
        "⚡ Skills": [
            "Grouped by category (Languages, Frameworks, Tools)",
            "Only list skills you can actually speak about in an interview",
            "Avoid rating yourself (no 'Python ⭐⭐⭐⭐')",
        ],
        "🏆 Achievements": [
            "At least 1 certification from a recognized platform",
            "Any hackathon wins, competition ranks, or academic awards",
            "Specific numbers where possible (Top 5%, 1st place, etc.)",
        ],
        "📐 Formatting": [
            "1 page only (freshers should never go to 2 pages)",
            "Consistent font (Calibri, Arial, or Helvetica recommended)",
            "No spelling/grammar errors — proofread twice",
            "Saved as PDF, not Word document",
        ],
    }

    for category, items in checklist_items.items():
        with st.expander(f"{category}"):
            for item in items:
                st.checkbox(item, key=f"check_{item[:20]}")

    st.markdown("---")
    st.markdown("## ❌ Common Fresher Resume Mistakes")

    mistakes = [
        ("Objective Statement", "Don't write 'Objective: To get a good job...' — replace with a Summary that tells your story."),
        ("Generic Skills", "Avoid listing 'MS Office' or 'Internet Browsing' — every person has these."),
        ("No Quantification", "Instead of 'Built a website', write 'Built a portfolio site with 500+ monthly visitors.'"),
        ("Lying About Skills", "If it's on your resume, you'll be asked about it. Only list what you know."),
        ("Photo on Resume", "Do NOT add your photo in India's tech hiring market — it's not expected and wastes space."),
        ("Multiple Pages", "Freshers should have exactly 1 page. Recruiters spend 7 seconds on a resume."),
        ("Fancy Templates with Tables/Columns", "These break ATS systems. Use simple, clean templates like the ones here."),
    ]

    for title, desc in mistakes:
        st.markdown(
            f"""
            <div style='
                background:#fff5f5; border-left:4px solid #e74c3c;
                border-radius:8px; padding:12px 16px; margin-bottom:10px;
            '>
                <b style='color:#e74c3c;'>❌ {title}</b><br/>
                <span style='color:#555;'>{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("## 🔗 Recommended Resources for Freshers")
    resources = [
        ("📚 Google Data Analytics Certificate", "coursera.org — Free to audit, paid for certificate"),
        ("🐍 Python for Everybody", "coursera.org — Best beginner Python course"),
        ("💼 LinkedIn Learning", "linkedin.com/learning — Free with LinkedIn Premium"),
        ("🧑‍💻 HackerRank", "hackerrank.com — Get skill badges for Python, SQL, Java"),
        ("🚀 GitHub Student Pack", "education.github.com — Free tools for students"),
        ("📊 Kaggle", "kaggle.com — Free datasets, notebooks, and ML competitions"),
    ]
    for name, desc in resources:
        st.markdown(f"- **{name}** — {desc}")
