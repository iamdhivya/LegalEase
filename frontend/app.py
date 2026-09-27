import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import streamlit as st

from config import WEB_LOGO_PATH, BACKEND_URL
from ai_core.generator import sanitize_text, format_docx, format_pdf, format_html_preview

st.set_page_config(page_title="LegalEase", layout="centered")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(WEB_LOGO_PATH):
        st.image(WEB_LOGO_PATH, use_container_width=True)

st.markdown(
    "<h2 style='text-align: center;'>AI Legal Document Generator</h2>",
    unsafe_allow_html=True,
)

document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False

if st.button("Generate Document"):
    if not all([document_type, parties, terms, dates]):
        st.warning("Please fill in all fields before generating.")
    else:
        with st.spinner("Generating document..."):
            response = None
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=60,
                )
                response.raise_for_status()
                st.session_state.generated_text = sanitize_text(response.json()["document"])
                st.success("Document Generated Successfully!")
            except requests.exceptions.HTTPError:
                try:
                    detail = response.json().get("detail", "Unknown error")
                except Exception:
                    detail = response.text if response is not None else "Unknown error"
                st.error(f"Backend error: {detail}")
            except Exception as e:
                st.error(f"Failed to generate document: {e}")

if st.session_state.generated_text:
    styled_html = format_html_preview(st.session_state.generated_text)
    st.markdown(styled_html, unsafe_allow_html=True)

    if st.button("Click to Edit Document"):
        st.session_state.show_edit = True

    if st.session_state.show_edit:
        edited_text = st.text_area(
            "Edit Document Below:", st.session_state.generated_text, height=300
        )
        st.session_state.generated_text = edited_text

    safe_filename = document_type.replace(" ", "_").lower() or "document"

    st.download_button(
        "Download as .TXT",
        data=st.session_state.generated_text,
        file_name=f"{safe_filename}.txt",
    )
    st.download_button(
        "Download as .DOCX",
        data=format_docx(st.session_state.generated_text, document_type),
        file_name=f"{safe_filename}.docx",
    )
    st.download_button(
        "Download as .PDF",
        data=format_pdf(st.session_state.generated_text, document_type),
        file_name=f"{safe_filename}.pdf",
    )
else:
    st.info("Click 'Generate Document' to start")