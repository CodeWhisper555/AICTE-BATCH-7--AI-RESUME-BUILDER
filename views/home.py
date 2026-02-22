"""
views/home.py — Landing Page
"""
import streamlit as st


def show():
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style='text-align:center; padding: 40px 0 10px 0;'>
            <span style='font-size:4rem;'>🎓</span>
            <h1 style='color:#6C63FF; font-size:3rem; margin:0;'>SmartResumeAI</h1>
            <h3 style='color:#444; font-weight:400;'>
                The All-in-One AI Resume Builder for <span style='color:#6C63FF;'>Students & Freshers</span>
            </h3>
            <p style='color:gray; font-size:1.05rem; max-width:600px; margin:auto;'>
                Build a professional, ATS-optimized resume in minutes using Google Gemini AI.
                No experience needed. Completely free.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Feature Cards ─────────────────────────────────────────────────────────
    st.markdown("<h2 style='text-align:center;'>✨ What You Can Do</h2>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    features = [
        ("📝", "Resume Builder", "Step-by-step form to collect all your details — education, projects, skills & more. AI enhances every section."),
        ("🎨", "5 Resume Templates", "Choose from Classic, Purple, Blue, Green, or Red PDF templates. All ATS-friendly."),
        ("✉️", "Cover Letter Generator", "Auto-generate a personalized cover letter for any job in seconds."),
        ("🎯", "ATS Score Checker", "Paste a job description and check how well your resume matches it. Get a score + missing keywords."),
        ("💡", "LinkedIn Summary", "Generate a compelling LinkedIn 'About' section from your resume details."),
        ("📖", "Step-by-Step Guide", "New to resumes? Our guide walks you through everything a fresher needs to know."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style='
                    background: linear-gradient(135deg, #f8f7ff, #ffffff);
                    border: 1px solid #e0dcff;
                    border-radius: 14px;
                    padding: 22px 18px;
                    margin-bottom: 18px;
                    box-shadow: 0 2px 8px rgba(108,99,255,0.07);
                    min-height: 160px;
                '>
                    <div style='font-size:2rem;'>{icon}</div>
                    <h4 style='color:#6C63FF; margin:8px 0 6px 0;'>{title}</h4>
                    <p style='color:#555; font-size:0.9rem; margin:0;'>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── How it works ──────────────────────────────────────────────────────────
    st.markdown("<h2 style='text-align:center;'>🚀 How It Works</h2>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    steps = [
        ("1️⃣", "Fill Your Details", "Enter your education, skills, projects, internships and more in a guided form."),
        ("2️⃣", "Let AI Enhance It", "Gemini AI rewrites and polishes every section to sound professional and impactful."),
        ("3️⃣", "Pick a Template", "Choose from 5 beautiful PDF templates and download your resume instantly."),
        ("4️⃣", "Check Your ATS Score", "Paste the job description and make sure your resume beats the ATS filter."),
        ("5️⃣", "Generate Cover Letter", "Get a tailored cover letter to go with every job application."),
    ]

    step_cols = st.columns(5)
    for i, (num, title, desc) in enumerate(steps):
        with step_cols[i]:
            st.markdown(
                f"""
                <div style='text-align:center; padding:10px;'>
                    <div style='font-size:2rem;'>{num}</div>
                    <b style='color:#6C63FF;'>{title}</b>
                    <p style='color:gray; font-size:0.82rem; margin-top:6px;'>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── CTA ───────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style='text-align:center; padding:30px 0;'>
            <h3 style='color:#6C63FF;'>Ready to build your resume? 🎯</h3>
            <p style='color:gray;'>Click <b>📝 Build My Resume</b> in the sidebar to get started!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Stats ─────────────────────────────────────────────────────────────────
    st.markdown("<br/>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, val, label in [
        (s1, "5", "Resume Templates"),
        (s2, "6", "AI-Powered Features"),
        (s3, "100%", "Free to Use"),
        (s4, "⚡ Fast", "PDF in Seconds"),
    ]:
        col.markdown(
            f"""
            <div style='text-align:center; background:#f0eeff; border-radius:12px; padding:18px;'>
                <h2 style='color:#6C63FF; margin:0;'>{val}</h2>
                <small style='color:#555;'>{label}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
