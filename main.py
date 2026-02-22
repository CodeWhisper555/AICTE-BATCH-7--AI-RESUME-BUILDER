"""
main.py — SmartResumeAI Entry Point
=====================================
Author: [Your Name]
Project: SmartResumeAI — AI-Powered Resume Builder for Students & Freshers
Powered by: Google Gemini API + Streamlit
"""

import streamlit as st

st.set_page_config(
    page_title="SmartResumeAI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar Navigation ────────────────────────────────────────────────────────
def sidebar():
    st.sidebar.markdown(
        """
        <div style='text-align:center; padding: 10px 0 5px 0;'>
            <span style='font-size:2.5rem;'>🎓</span>
            <h2 style='color:#6C63FF; margin:0;'>SmartResumeAI</h2>
            <small style='color:gray;'>For Students & Freshers</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    pages = {
        "🏠  Home": "home",
        "📝  Build My Resume": "builder",
        "🎨  Resume Templates": "templates",
        "✉️  Cover Letter": "cover_letter",
        "🎯  ATS Score Checker": "ats",
        "💡  LinkedIn Summary": "linkedin",
        "📖  How It Works": "guide",
    }

    st.sidebar.markdown("### 📌 Navigation")
    selection = st.sidebar.radio("", list(pages.keys()), label_visibility="collapsed")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align:center;'>
            <small style='color:gray;'>
                Powered by<br/>
                <b style='color:#6C63FF;'>Google Gemini AI</b> + Streamlit<br/><br/>
                Made for students 🚀
            </small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return pages[selection]


# ── Router ────────────────────────────────────────────────────────────────────
def main():
    page = sidebar()

    if page == "home":
        from views.home import show; show()
    elif page == "builder":
        from views.builder import show; show()
    elif page == "templates":
        from views.templates import show; show()
    elif page == "cover_letter":
        from views.cover_letter import show; show()
    elif page == "ats":
        from views.ats_checker import show; show()
    elif page == "linkedin":
        from views.linkedin_summary import show; show()
    elif page == "guide":
        from views.guide import show; show()


if __name__ == "__main__":
    main()
