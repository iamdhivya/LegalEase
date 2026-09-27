import sys
import os

# Allow imports of ai_core/ and config.py from the project root when this
# file is run directly (e.g. `uvicorn legalEaseAPI.main:app`).
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase - AI Legal Document Generator")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
