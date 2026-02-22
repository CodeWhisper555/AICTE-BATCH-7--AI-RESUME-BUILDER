"""
views/cover_letter.py — Cover Letter Generator
"""
import streamlit as st
from utils.gemini_client import generate


def show():
    st.markdown(
        """
        <h1 style='color:#6C63FF;'>✉️ Cover Letter Generator</h1>
        <p style='color:gray;'>
            Generate a personalized, professional cover letter for any job in seconds using Gemini AI.
        </p>
        <hr/>
        """,
        unsafe_allow_html=True,
    )

    # ── Tips ──────────────────────────────────────────────────────────────────
    with st.expander("💡 Tips for a great cover letter"):
        st.markdown(
            """
            - Keep it under **350 words** — recruiters spend ~30 seconds reading
            - **Match the tone** to the company (startup = casual, bank = formal)
            - Always **mention something specific** about the company
            - End with a **clear call to action** (request for interview)
            - Never just repeat your resume — tell a **story**
            """
        )

    st.markdown("---")

    # ── Form ──────────────────────────────────────────────────────────────────
    with st.form("cover_letter_form"):
        st.subheader("👤 Your Information")
        c1, c2 = st.columns(2)
        with c1:
            name       = st.text_input("Your Full Name *", placeholder="Priya Sharma")
            role       = st.text_input("Job Role Applying For *", placeholder="Data Science Intern")
            experience = st.selectbox("Experience Level", [
                "Fresher (0 years)", "Internship experience only",
                "1-2 years", "3-5 years"
            ])
        with c2:
            company    = st.text_input("Company Name *", placeholder="Google / TCS / Startup XYZ")
            skills     = st.text_input("Your Top 3-5 Skills *", placeholder="Python, ML, SQL, Communication")
            tone       = st.selectbox("Letter Tone", [
                "Professional & Formal",
                "Enthusiastic & Energetic",
                "Confident & Concise",
                "Creative & Unique",
            ])

        degree      = st.text_input("Your Degree & College", placeholder="B.Tech CSE from JNTU Hyderabad (2024)")
        achievement = st.text_input("Your Best Achievement (optional)", placeholder="Built a sentiment analysis model with 90% accuracy")
        company_reason = st.text_area(
            "Why this company? (optional but highly recommended)",
            placeholder="I admire Google's work on AI products like Bard and would love to contribute to...",
            height=70,
        )

        submitted = st.form_submit_button("✉️ Generate My Cover Letter", use_container_width=True)

    # ── Generate ──────────────────────────────────────────────────────────────
    if submitted:
        if not name or not role or not company or not skills:
            st.error("⚠️ Please fill in all required fields (Name, Role, Company, Skills).")
        else:
            tone_map = {
                "Professional & Formal":    "very formal and professional",
                "Enthusiastic & Energetic":  "enthusiastic, warm and energetic",
                "Confident & Concise":       "confident, direct and concise",
                "Creative & Unique":         "creative and memorable while staying professional",
            }

            company_note = f"\nWhy this company (use this): {company_reason}" if company_reason else ""
            achievement_note = f"\nKey achievement to highlight: {achievement}" if achievement else ""

            prompt = f"""
Write a compelling cover letter for a student/fresher with these details:

Name: {name}
Applying For: {role} at {company}
Education: {degree if degree else 'Engineering student'}
Experience: {experience}
Key Skills: {skills}
Tone: {tone_map[tone]}
{achievement_note}
{company_note}

Requirements:
- Structure: Opening (hook + role), Body paragraph 1 (skills/projects), Body paragraph 2 (why this company), Closing (CTA)
- Total length: 280-320 words
- Do NOT use placeholder text like [Your Address] or [Date]
- Start directly with "Dear Hiring Manager," or "Dear [Company] Recruitment Team,"
- End with a strong call to action and the candidate's name
- Sound human and genuine, not like a template
- Incorporate the skills naturally — don't just list them

Return ONLY the cover letter text.
"""
            letter = generate(prompt, "✍️ Writing your cover letter...")

            st.success("✅ Your cover letter is ready!")
            st.markdown("---")

            st.subheader("📄 Your Cover Letter")
            st.markdown(
                f"""
                <div style='
                    background:#f8f9ff;
                    border-left:4px solid #6C63FF;
                    padding:24px 28px;
                    border-radius:10px;
                    font-size:15px;
                    line-height:1.9;
                    color:#222;
                    white-space:pre-wrap;
                '>{letter}</div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("---")
            ca, cb = st.columns(2)
            with ca:
                st.text_area("📋 Copy from here:", value=letter, height=200)
            with cb:
                st.download_button(
                    "⬇️ Download as .txt",
                    data=letter,
                    file_name=f"{name.replace(' ','_')}_Cover_Letter.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
                st.info("💡 Paste into Google Docs → File → Download → PDF for a polished version.")

            st.caption("Not satisfied? Adjust details in the form above and regenerate.")
