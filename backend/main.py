from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="LegalEase API",
    version="1.0.0",
    description="AI-powered legal document draft generator",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = Field(..., min_length=2)
    effective_date: str = Field(..., min_length=2)
    jurisdiction: str = ""
    additional_instructions: str = ""

class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    mock: bool
    disclaimer: str

def generate_document(request: DocumentRequest):
    terms = []
    for item in request.terms.split(";"):
        item = item.strip()
        if item:
            terms.append("- " + item)
    if not terms:
        terms.append("- [NOT PROVIDED]")

    terms_text = "\n".join(terms)

    document = f"""
{request.document_type.upper()}

PARTIES

{request.parties}

EFFECTIVE DATE

{request.effective_date}

RECITALS

The parties identified above wish to enter into this
{request.document_type} on the effective date stated above.

TERMS AND CONDITIONS

{terms_text}

JURISDICTION

{request.jurisdiction or "[NOT PROVIDED]"}

ADDITIONAL INSTRUCTIONS

{request.additional_instructions or "[NONE]"}

TERM AND TERMINATION

The parties should confirm the applicable term and
termination conditions before signing.

SIGNATURES

PARTY 1

Signature: ______________________________

Name: __________________________________

Date: __________________________________

PARTY 2

Signature: ______________________________

Name: __________________________________

Date: __________________________________

IMPORTANT REVIEW NOTICE

This is an AI-generated draft for informational purposes only.

It is not legal advice and should be reviewed and customized
by a qualified legal professional before signing or relying
on this document.
"""

    return document.strip()

@app.get("/")
def root():
    return {
        "app": "LegalEase",
        "status": "running",
        "service": "LegalEase API",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "ok", "ai_mode": "mock", "model": "mock"}

@app.post("/api/generate", response_model=DocumentResponse)
def generate(request: DocumentRequest):
    try:
        content = generate_document(request)
        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            model="mock",
            mock=True,
            disclaimer=(
                "AI-generated draft for informational purposes only. "
                "This is not legal advice. "
                "Review with a qualified legal professional "
                "before signing or relying on this document."
            ),
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
