"""
views/templates.py — Resume Template Showcase
"""
import streamlit as st
from utils.pdf_generator import TEMPLATES, build_pdf


def show():
    st.markdown(
        """
        <h1 style='color:#6C63FF;'>🎨 Resume Templates</h1>
        <p style='color:gray;'>
            All 5 templates are ATS-friendly. Choose based on the industry you're applying to.
        </p>
        <hr/>
        """,
        unsafe_allow_html=True,
    )

    template_info = {
        "🎯 Classic Professional": {
            "best_for": "Government, Banking, Traditional companies, Law",
            "colors": "Black & White",
            "ats": "⭐⭐⭐⭐⭐ Best ATS Score",
            "tip": "Safe choice for any industry. Cannot go wrong.",
        },
        "💜 Modern Purple": {
            "best_for": "Tech companies, Startups, Product Management, Design",
            "colors": "Purple & White",
            "ats": "⭐⭐⭐⭐ Excellent ATS Score",
            "tip": "Most popular choice for software/data roles.",
        },
        "🌊 Corporate Blue": {
            "best_for": "Consulting, Engineering, MBA programs, Finance",
            "colors": "Navy Blue & White",
            "ats": "⭐⭐⭐⭐ Excellent ATS Score",
            "tip": "Projects seriousness and credibility.",
        },
        "🍃 Minimal Green": {
            "best_for": "Healthcare, Education, NGOs, Sustainability",
            "colors": "Green & White",
            "ats": "⭐⭐⭐⭐ Excellent ATS Score",
            "tip": "Clean, calm aesthetic — great for people-oriented roles.",
        },
        "🔥 Bold Red": {
            "best_for": "Marketing, Sales, PR, Creative roles",
            "colors": "Red & White",
            "ats": "⭐⭐⭐⭐ Excellent ATS Score",
            "tip": "Shows confidence and energy. Great for client-facing roles.",
        },
    }

    # ── Template Cards ────────────────────────────────────────────────────────
    cols = st.columns(3)
    for i, (tname, tdata) in enumerate(template_info.items()):
        t = TEMPLATES[tname]
        r, g, b = t["header_bg"]
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style='
                    border:1px solid #e0e0e0;
                    border-radius:14px;
                    overflow:hidden;
                    margin-bottom:20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
                '>
                    <div style='
                        background:rgb({r},{g},{b});
                        padding:20px;
                        text-align:center;
                    '>
                        <div style='font-size:2rem;'>{tname.split()[0]}</div>
                        <b style='color:{"white" if t["style"]=="modern" else "black"}; font-size:1rem;'>
                            {" ".join(tname.split()[1:])}
                        </b>
                    </div>
                    <div style='padding:16px;'>
                        <p style='color:#555; font-size:0.85rem; margin:4px 0;'>
                            🎯 <b>Best for:</b> {tdata["best_for"]}
                        </p>
                        <p style='color:#555; font-size:0.85rem; margin:4px 0;'>
                            🎨 <b>Colors:</b> {tdata["colors"]}
                        </p>
                        <p style='color:#555; font-size:0.85rem; margin:4px 0;'>
                            🤖 <b>ATS:</b> {tdata["ats"]}
                        </p>
                        <p style='color:#6C63FF; font-size:0.82rem; margin-top:8px; font-style:italic;'>
                            💡 {tdata["tip"]}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Quick Sample PDF ──────────────────────────────────────────────────────
    st.subheader("📥 Download a Sample Resume")
    st.markdown("*See how each template looks with sample data before you build yours.*")

    selected = st.selectbox("Choose template to preview", list(TEMPLATES.keys()))

    if st.button("⬇️ Download Sample PDF", use_container_width=True):
        sample_data = {
            "name": "Priya Sharma",
            "email": "priya@gmail.com",
            "phone": "+91 9876543210",
            "location": "Hyderabad, India",
            "linkedin": "linkedin.com/in/priyasharma",
            "github": "github.com/priyasharma",
            "summary": "Final year B.Tech CSE student with a strong foundation in Python, Machine Learning, and web development. Built 3+ end-to-end ML projects and completed a data science internship at a tech startup. Seeking a full-time SDE/Data Science role where I can apply my skills to solve real-world problems.",
            "education": [
                {"degree": "B.Tech Computer Science", "institution": "JNTU Hyderabad", "year": "2020 – 2024", "grade": "8.5 / 10"},
                {"degree": "Class 12 (MPC)", "institution": "Narayana Junior College", "year": "2018 – 2020", "grade": "95.4%"},
            ],
            "experience": [
                {"role": "Data Science Intern", "company": "TechStartup Pvt. Ltd.", "duration": "May – Aug 2023",
                 "description": "• Built a customer churn prediction model using XGBoost with 89% accuracy, reducing churn by 12%\n• Automated weekly reporting dashboards using Python and Tableau, saving 5 hours per week\n• Collaborated with a team of 4 engineers in an Agile environment"}
            ],
            "projects": "• Fake News Detector (Python, NLP, LSTM): Classified news articles as real/fake with 94% accuracy. Deployed as a Flask web app.\n• Stock Price Predictor (Python, LSTM, yfinance): Predicted next-day stock prices with RMSE of 2.3 for NIFTY 50.\n• Personal Finance Tracker (React, Firebase): Built a full-stack app to track expenses with visualizations.",
            "skills": "Languages: Python, Java, SQL, JavaScript\nFrameworks: TensorFlow, Scikit-learn, React, Flask\nTools: Git, Docker, Jupyter, VS Code, Tableau\nSoft Skills: Problem Solving, Team Collaboration, Communication",
            "achievements": "• Google Data Analytics Professional Certificate – Coursera (2023)\n• Ranked Top 5% in HackerRank Python Assessment (Gold Badge)\n• 1st Place – College Hackathon 2023 (50+ teams)",
            "extra": "• Technical Lead, College Coding Club (2022-23) — organized workshops for 200+ students\n• NSS Volunteer — coordinated blood donation drives and awareness campaigns",
        }
        pdf_bytes = build_pdf(sample_data, selected)
        st.download_button(
            f"📄 Download {selected} Sample",
            data=pdf_bytes,
            file_name=f"Sample_Resume_{selected.replace(' ', '_').replace('/', '')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.markdown("---")
    st.info("🚀 Ready to build your own? Click **📝 Build My Resume** in the sidebar!")
