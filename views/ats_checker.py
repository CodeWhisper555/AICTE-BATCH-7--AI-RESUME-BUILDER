"""
views/ats_checker.py — ATS Score Checker
"""
import streamlit as st
from utils.gemini_client import generate
import re


def parse_score(text):
    """Extract numeric score from Gemini response."""
    match = re.search(r'\b(\d{1,3})\s*(?:/\s*100|%|out of 100)', text, re.IGNORECASE)
    if match:
        return min(int(match.group(1)), 100)
    return None


def show():
    st.markdown(
        """
        <h1 style='color:#6C63FF;'>🎯 ATS Score Checker</h1>
        <p style='color:gray;'>
            ATS (Applicant Tracking System) filters resumes before a human ever sees them.
            Paste your resume and the job description below to get your match score and fix suggestions.
        </p>
        <hr/>
        """,
        unsafe_allow_html=True,
    )

    # ── What is ATS? ──────────────────────────────────────────────────────────
    with st.expander("❓ What is ATS and why does it matter?"):
        st.markdown(
            """
            **ATS (Applicant Tracking System)** is software used by companies to automatically
            filter resumes based on keywords, skills, and relevance to the job description.

            **Key facts for freshers:**
            - Over **75% of resumes** are rejected by ATS before reaching a recruiter
            - ATS looks for **exact keyword matches** from the job description
            - A score of **80%+ is considered good**
            - Use the **Classic Professional** template for best ATS compatibility

            **How to improve your score:**
            - Mirror keywords from the job description naturally in your resume
            - Avoid tables, images, or fancy formatting in ATS-submitted resumes
            - Use standard section headings (Education, Experience, Skills)
            """
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Your Resume Content")
        resume_text = st.text_area(
            "Paste your resume text here",
            height=300,
            placeholder="Paste the text content of your resume here...\n\nTip: Open your resume PDF, select all (Ctrl+A), copy and paste here.",
            key="resume_text",
        )

    with col2:
        st.subheader("📋 Job Description")
        job_desc = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="Paste the full job description from LinkedIn, Naukri, or any job portal here...",
            key="job_desc",
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.button("🎯 Check My ATS Score", use_container_width=True, type="primary"):
        if not resume_text.strip() or not job_desc.strip():
            st.error("⚠️ Please paste both your resume text and the job description.")
        else:
            prompt = f"""
You are an expert ATS (Applicant Tracking System) analyzer.

Analyze how well this resume matches the given job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Provide a detailed analysis in this EXACT format:

ATS MATCH SCORE: [X]/100

MATCHED KEYWORDS:
[List keywords/skills found in both resume and JD, one per line with •]

MISSING KEYWORDS:
[List important keywords from JD missing in resume, one per line with •]

SKILL GAPS:
[List specific skills/qualifications missing, one per line with •]

STRENGTHS:
[2-3 things the resume does well for this role, one per line with •]

RECOMMENDATIONS:
[5 specific, actionable suggestions to improve the resume for this role, numbered 1-5]

VERDICT:
[One paragraph honest assessment — should they apply? What's their chance?]
"""
            result = generate(prompt, "🔍 Analyzing your resume against the job description...")

            # ── Parse score ───────────────────────────────────────────────────
            score = parse_score(result)

            st.markdown("---")
            st.subheader("📊 Your ATS Analysis")

            # Score gauge
            if score is not None:
                if score >= 80:
                    color, emoji, label = "#27ae60", "🟢", "Excellent Match!"
                elif score >= 60:
                    color, emoji, label = "#f39c12", "🟡", "Good Match — Minor Improvements Needed"
                elif score >= 40:
                    color, emoji, label = "#e67e22", "🟠", "Average — Significant Improvements Needed"
                else:
                    color, emoji, label = "#e74c3c", "🔴", "Poor Match — Major Changes Required"

                st.markdown(
                    f"""
                    <div style='
                        text-align:center;
                        background:linear-gradient(135deg, {color}15, {color}30);
                        border: 2px solid {color};
                        border-radius:16px;
                        padding:24px;
                        margin-bottom:20px;
                    '>
                        <div style='font-size:3.5rem; font-weight:bold; color:{color};'>{emoji} {score}/100</div>
                        <div style='font-size:1.1rem; color:{color}; font-weight:600;'>{label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Progress bar
                st.progress(score / 100)

            # Full analysis
            st.markdown(
                f"""
                <div style='
                    background:#f8f9ff;
                    border-left:4px solid #6C63FF;
                    border-radius:8px;
                    padding:20px 24px;
                    line-height:1.8;
                    white-space:pre-wrap;
                    font-size:0.95rem;
                '>{result}</div>
                """,
                unsafe_allow_html=True,
            )

            # Download report
            st.download_button(
                "⬇️ Download ATS Report as .txt",
                data=result,
                file_name="ATS_Score_Report.txt",
                mime="text/plain",
            )
