import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase - AI Legal Document Generator")

# Enable CORS so your frontend on Render can talk to this backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://legalease-3-uh8k.onrender.com",  # Your frontend application URL
        "http://localhost:8501",                  # Local Streamlit testing
        "http://localhost:3000",                  # Local React/Next.js testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}


if __name__ == "__main__":
    import uvicorn
    # Keep host as "0.0.0.0" and port as 8000 (or use os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
