"""
views/linkedin_summary.py — LinkedIn Summary Generator
"""
import streamlit as st
from utils.gemini_client import generate


def show():
    st.markdown(
        """
        <h1 style='color:#6C63FF;'>💡 LinkedIn Summary Generator</h1>
        <p style='color:gray;'>
            Your LinkedIn 'About' section is the first thing recruiters read.
            Let Gemini AI craft one that gets you noticed.
        </p>
        <hr/>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("💡 What makes a great LinkedIn summary?"):
        st.markdown(
            """
            - **Hook in the first line** — LinkedIn shows only 2 lines before "see more"
            - **Tell your story** — not just what you've done, but where you're going
            - **Include keywords** — recruiters search LinkedIn with terms like "Python Developer" or "Data Science Fresher"
            - **End with a CTA** — "Open to opportunities in..." or "Let's connect!"
            - **Length:** 150-250 words is ideal
            """
        )

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        name       = st.text_input("Your Name", placeholder="Priya Sharma")
        degree     = st.text_input("Degree & College", placeholder="B.Tech CSE, JNTU Hyderabad (2024)")
        target     = st.text_input("Target Role / Industry *", placeholder="Data Science | ML Engineer | Python Developer")
        skills     = st.text_input("Top Skills *", placeholder="Python, Machine Learning, SQL, TensorFlow")
    with c2:
        projects   = st.text_area("Key Projects (1-2 lines)", placeholder="Built a fake news detector (94% accuracy) | Stock price prediction app", height=80)
        achievement = st.text_area("Achievements / Certifications", placeholder="Google Data Analytics Certificate | Top 5% HackerRank", height=80)
        personality = st.selectbox("Your personality vibe", ["Ambitious & Driven", "Curious & Analytical", "Creative Problem Solver", "Team Player & Leader"])

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.button("💡 Generate LinkedIn Summary", use_container_width=True, type="primary"):
        if not target or not skills:
            st.error("⚠️ Please fill in Target Role and Skills at minimum.")
        else:
            prompt = f"""
Write a compelling LinkedIn 'About' section for a student/fresher:

Name: {name if name else 'the candidate'}
Education: {degree if degree else 'Engineering student'}
Target: {target}
Skills: {skills}
Projects: {projects if projects else 'Built multiple academic projects'}
Achievements: {achievement if achievement else ''}
Personality: {personality}

Requirements:
- 180-230 words
- First sentence must be a STRONG hook (not "I am a student...")
- Include relevant keywords from their target role naturally
- Mention 1-2 specific projects/achievements
- End with: "Open to [role] opportunities. Let's connect!"
- Write in first person
- Sound authentic, not robotic

Return ONLY the LinkedIn summary text.
"""
            summary = generate(prompt, "✍️ Crafting your LinkedIn summary...")

            st.success("✅ Your LinkedIn summary is ready!")
            st.markdown("---")

            st.markdown(
                f"""
                <div style='
                    background:#f0f7ff;
                    border-left:4px solid #0077b5;
                    padding:22px 26px;
                    border-radius:10px;
                    font-size:15px;
                    line-height:1.85;
                    color:#222;
                    white-space:pre-wrap;
                '>{summary}</div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("---")
            st.text_area("📋 Copy from here:", value=summary, height=180)
            st.download_button(
                "⬇️ Download as .txt",
                data=summary,
                file_name="LinkedIn_Summary.txt",
                mime="text/plain",
            )
            st.info("💡 Go to LinkedIn → Edit Profile → About → Paste this text.")
