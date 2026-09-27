import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = "gemini-3.5-flash"

# Paths (relative to project root — run.sh / uvicorn / streamlit are expected
# to be launched from the LegalEase/ folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "Image", "Logo.png")
INVERSE_LOGO_PATH = os.path.join(BASE_DIR, "Image", "inverseLogo.png")
WEB_LOGO_PATH = LOGO_PATH  # used by the Streamlit header

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
