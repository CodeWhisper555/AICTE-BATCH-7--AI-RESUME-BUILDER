import streamlit as st
from google import genai


@st.cache_resource
def get_client():
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

    return genai.Client(api_key=api_key)


def generate(prompt: str, spinner_text: str = "🤖 Generating with Gemini AI...") -> str:
    client = get_client()
    with st.spinner(spinner_text):
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
    return response.text.strip()
