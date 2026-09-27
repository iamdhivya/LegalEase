#!/bin/bash
# Launches the FastAPI backend and Streamlit frontend together.
# Run from the LegalEase/ project root: bash run.sh

set -e

echo "Starting FastAPI backend on http://localhost:8000 ..."
uvicorn legalEaseAPI.main:app --reload &
BACKEND_PID=$!

sleep 2

echo "Starting Streamlit frontend on http://localhost:8501 ..."
streamlit run frontend/app.py

# When the Streamlit process exits, also stop the backend.
kill $BACKEND_PID
