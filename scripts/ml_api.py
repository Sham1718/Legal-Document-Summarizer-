from fastapi import FastAPI
from pydantic import BaseModel
from rag_core import ask_rag
from pydantic import BaseModel
from summary_core import summarize_textrank, summarize_t5
from explain_core import explain_textrank
from pdfminer.high_level import extract_text as pdf_text
from docx import Document


app = FastAPI(title="Legal Document ML API")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

class SummaryRequest(BaseModel):
    text: str
    method: str = "textrank"  # "textrank" or "t5"

class SummaryResponse(BaseModel):
    summary: str

class ExplainRequest(BaseModel):
    text: str

class ExplainResponse(BaseModel):
    explanation: list


@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    answer, sources = ask_rag(req.question)
    return {
        "answer": answer,
        "sources": sources
    }

@app.post("/summarize", response_model=SummaryResponse)
def summarize(req: SummaryRequest):
    if req.method.lower() == "t5":
        return {"summary": summarize_t5(req.text)}
    return {"summary": summarize_textrank(req.text)}

@app.post("/explain-summary", response_model=ExplainResponse)
def explain_summary(req: ExplainRequest):
    explanation = explain_textrank(req.text)
    return {"explanation": explanation}

@app.post("/document/process")
def process_document(req: dict):
    path = req["path"]

    text = extract_text(path)

    summary = summarize(text)
    explanation = explain(text)

    return {
        "summary": summary,
        "explanation": explanation
    }

def extract_text(path):
    if path.endswith(".pdf"):
        return pdf_text(path)

    if path.endswith(".docx"):
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    if path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    raise ValueError("Unsupported file type")

def summarize(text: str) -> str:
    """
    Default summarization for document upload.
    Uses T5 for better quality.
    """
    return summarize_t5(text)


def explain(text: str):
    """
    Explanation using TextRank-based explainability.
    Returns structured explanation.
    """
    return explain_textrank(text)


