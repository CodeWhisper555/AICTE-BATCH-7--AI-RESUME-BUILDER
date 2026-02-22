# 🎓 SmartResumeAI — AI-Powered Resume Builder for Students & Freshers

> Built with **Google Gemini AI** + **Streamlit** | Designed for students, by students

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Resume Builder** | Step-by-step guided form with AI enhancement for every section |
| 🎨 **5 PDF Templates** | Classic, Purple, Blue, Green, Red — all ATS-friendly |
| 🎯 **ATS Score Checker** | Paste any job description and get a match score + missing keywords |
| ✉️ **Cover Letter Generator** | Personalized cover letter in 4 different tones |
| 💡 **LinkedIn Summary** | AI-crafted LinkedIn 'About' section |
| 📖 **Fresher's Guide** | Complete resume guide + interactive checklist |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/SmartResumeAI.git
cd SmartResumeAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Your Gemini API Key

Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

Or enter it directly in the sidebar when you run the app.

### 4. Run the App
```bash
streamlit run main.py
```

---

## 📁 Project Structure

```
SmartResumeAI/
├── main.py                    # Entry point & navigation router
├── requirements.txt           # Dependencies
├── .streamlit/
│   ├── config.toml            # Theme (Purple + White)
│   └── secrets.toml           # API keys (gitignored)
├── views/
│   ├── home.py                # Landing page
│   ├── builder.py             # Resume builder with AI enhancement
│   ├── templates.py           # Template showcase & sample download
│   ├── cover_letter.py        # Cover letter generator
│   ├── ats_checker.py         # ATS score checker
│   ├── linkedin_summary.py    # LinkedIn summary generator
│   └── guide.py              # Fresher resume guide & checklist
└── utils/
    ├── gemini_client.py       # Shared Gemini API client
    └── pdf_generator.py       # PDF builder with 5 templates
```

---

## 🎨 Resume Templates

| Template | Best For | ATS Score |
|---|---|---|
| 🎯 Classic Professional | Government, Banking, Traditional | ⭐⭐⭐⭐⭐ |
| 💜 Modern Purple | Tech, Startups, Product | ⭐⭐⭐⭐ |
| 🌊 Corporate Blue | Consulting, Engineering, MBA | ⭐⭐⭐⭐ |
| 🍃 Minimal Green | Healthcare, Education, NGOs | ⭐⭐⭐⭐ |
| 🔥 Bold Red | Marketing, Sales, Creative | ⭐⭐⭐⭐ |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini 1.5 Flash
- **PDF Generation:** fpdf2
- **Language:** Python 3.10+

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 👤 Author

**[Ajay Chandra]**
- GitHub: [CodeWhisper555](https://github.com/CodeWhisper555)

---

> ⭐ If this project helped you, please give it a star on GitHub!
