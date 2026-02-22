import streamlit as st
import google.generativeai as genai


@st.cache_resource
def get_model():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.sidebar.markdown("---")
        api_key = st.sidebar.text_input(
            "🔑 Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Get your free key at aistudio.google.com",
        )
        if not api_key:
            st.warning("⚠️ Please enter your Gemini API key in the sidebar.")
            st.stop()

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def generate(prompt: str, spinner_text: str = "🤖 Generating with Gemini AI...") -> str:
    model = get_model()
    with st.spinner(spinner_text):
        response = model.generate_content(prompt)
    return response.text.strip()
