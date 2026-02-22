"""
utils/pdf_generator.py — Resume PDF Builder
============================================
Generates styled PDF resumes using fpdf2.
Called by both the builder and templates views.
"""

from fpdf import FPDF
import textwrap


TEMPLATES = {
    "🎯 Classic Professional": {
        "header_bg": (255, 255, 255),
        "header_text": (0, 0, 0),
        "accent": (0, 0, 0),
        "divider": (0, 0, 0),
        "style": "classic",
    },
    "💜 Modern Purple": {
        "header_bg": (108, 99, 255),
        "header_text": (255, 255, 255),
        "accent": (108, 99, 255),
        "divider": (108, 99, 255),
        "style": "modern",
    },
    "🌊 Corporate Blue": {
        "header_bg": (26, 82, 160),
        "header_text": (255, 255, 255),
        "accent": (26, 82, 160),
        "divider": (26, 82, 160),
        "style": "modern",
    },
    "🍃 Minimal Green": {
        "header_bg": (39, 174, 96),
        "header_text": (255, 255, 255),
        "accent": (39, 174, 96),
        "divider": (39, 174, 96),
        "style": "modern",
    },
    "🔥 Bold Red": {
        "header_bg": (192, 57, 43),
        "header_text": (255, 255, 255),
        "accent": (192, 57, 43),
        "divider": (192, 57, 43),
        "style": "modern",
    },
}


class ResumePDF(FPDF):
    def __init__(self, t):
        super().__init__()
        self.t = t
        self.set_auto_page_break(auto=True, margin=15)

    def safe_text(self, text):
        return text.encode("latin-1", "replace").decode("latin-1")

    def header_block(self, name, email, phone, location, linkedin, github):
        t = self.t
        if t["style"] == "modern":
            self.set_fill_color(*t["header_bg"])
            self.rect(0, 0, 210, 45, "F")
            self.set_text_color(*t["header_text"])
            self.set_font("Helvetica", "B", 22)
            self.set_xy(12, 8)
            self.cell(0, 10, self.safe_text(name.upper()), ln=True)
            self.set_font("Helvetica", "", 8.5)
            parts = [p for p in [email, phone, location] if p]
            self.set_x(12)
            self.cell(0, 5, "  |  ".join(parts), ln=True)
            if linkedin or github:
                links = [p for p in [linkedin, github] if p]
                self.set_x(12)
                self.cell(0, 5, "  |  ".join(links), ln=True)
            self.ln(18)
        else:
            self.set_text_color(0, 0, 0)
            self.set_font("Helvetica", "B", 22)
            self.cell(0, 12, self.safe_text(name.upper()), ln=True, align="C")
            self.set_font("Helvetica", "", 9)
            parts = [p for p in [email, phone, location] if p]
            self.cell(0, 5, "  |  ".join(parts), ln=True, align="C")
            if linkedin or github:
                links = [p for p in [linkedin, github] if p]
                self.set_font("Helvetica", "", 8.5)
                self.cell(0, 5, "  |  ".join(links), ln=True, align="C")
            self.set_draw_color(*t["divider"])
            self.set_line_width(0.6)
            self.line(12, self.get_y() + 2, 198, self.get_y() + 2)
            self.ln(8)

    def section_title(self, title):
        t = self.t
        self.set_text_color(*t["accent"])
        self.set_font("Helvetica", "B", 11)
        self.set_x(12)
        self.cell(0, 8, title.upper(), ln=True)
        self.set_draw_color(*t["divider"])
        self.set_line_width(0.3)
        self.line(12, self.get_y(), 198, self.get_y())
        self.set_text_color(30, 30, 30)
        self.ln(3)

    def body(self, text, indent=0):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(40, 40, 40)
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line:
                self.ln(2)
                continue
            for wl in textwrap.wrap(self.safe_text(line), width=92):
                self.set_x(12 + indent)
                self.cell(0, 5.5, wl, ln=True)
        self.ln(3)

    def experience_entry(self, role, company, duration, desc):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(12)
        self.cell(130, 6, self.safe_text(f"{role}  —  {company}"), ln=False)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6, self.safe_text(duration), ln=True, align="R")
        self.body(desc, indent=4)

    def education_entry(self, degree, institution, year, grade):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        self.set_x(12)
        self.cell(130, 6, self.safe_text(degree), ln=False)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(110, 110, 110)
        self.cell(0, 6, self.safe_text(year), ln=True, align="R")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(60, 60, 60)
        self.set_x(16)
        extra = f"  |  {grade}" if grade else ""
        self.cell(0, 5, self.safe_text(f"{institution}{extra}"), ln=True)
        self.ln(2)


def build_pdf(data: dict, template_name: str) -> bytes:
    t = TEMPLATES[template_name]
    pdf = ResumePDF(t)
    pdf.add_page()

    pdf.header_block(
        data.get("name", ""), data.get("email", ""),
        data.get("phone", ""), data.get("location", ""),
        data.get("linkedin", ""), data.get("github", ""),
    )

    if data.get("summary"):
        pdf.section_title("Professional Summary")
        pdf.body(data["summary"])

    if data.get("education"):
        pdf.section_title("Education")
        for e in data["education"]:
            pdf.education_entry(e["degree"], e["institution"], e["year"], e.get("grade", ""))

    if data.get("experience"):
        pdf.section_title("Internships & Work Experience")
        for ex in data["experience"]:
            pdf.experience_entry(ex["role"], ex["company"], ex["duration"], ex["description"])

    if data.get("projects"):
        pdf.section_title("Projects")
        pdf.body(data["projects"])

    if data.get("skills"):
        pdf.section_title("Technical Skills")
        pdf.body(data["skills"])

    if data.get("achievements"):
        pdf.section_title("Achievements & Certifications")
        pdf.body(data["achievements"])

    if data.get("extra"):
        pdf.section_title("Extra-Curricular Activities")
        pdf.body(data["extra"])

    return bytes(pdf.output())
