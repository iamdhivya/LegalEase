import io
import os
import re
import html
import textwrap

from docx import Document
from docx.shared import Inches, Pt
from fpdf import FPDF

from config import LOGO_PATH


def sanitize_text(text: str) -> str:
    """Removes special/typographic characters that break clean formatting,
    and strips anything the PDF font (Latin-1 only) can't render."""
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2026": "...",
        "\u2022": "-",
        "\u00a0": " ",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    # Drop any remaining character the PDF's core font can't encode
    text = text.encode("latin-1", "ignore").decode("latin-1")
    return text.strip()

def _split_terms(terms: str):
    """Splits a semicolon-separated terms string into a clean list."""
    return [t.strip() for t in terms.split(";") if t.strip()]


def format_docx(text: str, doc_type: str) -> bytes:
    """Builds a Word document: logo + title, body in Times New Roman, a
    terms table if the raw terms are available in the text, and a footer."""
    doc = Document()

    if os.path.exists(LOGO_PATH):
        doc.add_picture(LOGO_PATH, width=Inches(1.5))

    title = doc.add_heading(doc_type, level=1)
    title.alignment = 1  # center

    for para in text.split("\n"):
        if not para.strip():
            continue
        p = doc.add_paragraph(para.strip())
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)

    footer = doc.sections[0].footer
    footer.paragraphs[0].text = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.getvalue()


class _PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, x=90, y=8, w=25)
            self.ln(20)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "LegalEase", new_x="LMARGIN", new_y="NEXT", align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, "LegalEase Inc. | contact@legalease.com | All Rights Reserved.", align="C")


def format_pdf(text: str, doc_type: str) -> bytes:
    """Builds a branded PDF with header logo and footer on every page.
    Text is wrapped manually in Python (not via FPDF's own line-breaker,
    which is unreliable on some inputs) so every line is guaranteed to fit."""
    pdf = _PDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    usable_width = pdf.epw  # effective page width between margins
    chars_per_line = max(20, int(usable_width / 1.9))

    def _wrapped(s: str):
        return textwrap.wrap(
            s.strip(), width=chars_per_line,
            break_long_words=True, break_on_hyphens=True,
        ) or [""]

    pdf.set_font("Helvetica", "B", 12)
    for line in _wrapped(doc_type or "Legal Document"):
        pdf.cell(pdf.epw, 10, line, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 11)
    for para in text.split("\n"):
        if not para.strip():
            pdf.ln(3)
            continue
        for line in _wrapped(para):
            pdf.cell(pdf.epw, 7, line, new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output(dest="S"))


def format_html_preview(text: str) -> str:
    """Converts raw text into a dark-themed scrollable HTML preview block."""
    escaped = html.escape(text)
    body = escaped.replace("\n", "<br>")
    return (
        "<div style='background-color:#111418;color:#e6e6e6;"
        "padding:20px;border-radius:8px;max-height:400px;overflow-y:auto;"
        "font-family:Georgia, serif;line-height:1.6;'>"
        f"{body}"
        "</div>"
    )
