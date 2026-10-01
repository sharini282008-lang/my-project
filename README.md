# LegalEase - Updated Working Version

This package contains the updated LegalEase project after the backend and frontend simplification changes.

## Run backend

```powershell
.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Open: http://127.0.0.1:8000/docs

## Run frontend

Open a second terminal:

```powershell
.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

Open: http://localhost:8501

## Current mode

The current backend uses MOCK generation so the complete local flow can be tested without a Gemini API key.

The frontend supports:
- Generate document
- Preview
- Edit
- Download TXT
- Download DOCX
- Download PDF
