# LegalEase — AI Legal Document Generator

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and paste in your Gemini API key:
   ```
   cp .env.example .env
   ```
4. (Optional) Drop your own `Logo.png` / `inverseLogo.png` into `Image/` —
   the app runs fine without them, it just skips the logo.

## Run

From the `LegalEase/` root:

```
bash run.sh
```

This starts the FastAPI backend (port 8000) and the Streamlit frontend
(port 8501). Open http://localhost:8501 in your browser.

Or start them separately, in two terminals:
```
uvicorn legalEaseAPI.main:app --reload
streamlit run frontend/app.py
```

## Project structure

```
LegalEase/
├── ai_core/
│   ├── gemini_generator.py   # calls the Gemini API
│   └── generator.py          # sanitize_text, format_docx/pdf/html_preview
├── legalEaseAPI/
│   ├── main.py                # FastAPI app
│   └── routes.py              # POST /generate
├── frontend/
│   └── app.py                 # Streamlit UI
├── Image/                      # optional logo files
├── config.py
├── requirements.txt
├── run.sh
└── .env.example
```
