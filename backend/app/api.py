from fastapi import APIRouter
from app.rag import answer_query
from app.data_ingestion import SOURCES, ingest_source
from pydantic import BaseModel
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    role: str

@router.post("/chat")
def chat(request: ChatRequest):
    print("Received chat request:", request.query, request.role)
    answer, references = answer_query(request.query, request.role)
    return {"answer": answer, "references": references}

class IngestRequest(BaseModel):
    source: str
    file_path: str = None

@router.post("/ingest")
def ingest(request: IngestRequest):
    source = request.source
    if source in SOURCES:
        if source == "whatsapp" and request.file_path:
            SOURCES[source].ingest(request.file_path)
        else:
            ingest_source(source)
        return {"status": "ingested"}
    return {"error": "Unknown source"}

@router.get("/sources")
def sources():
    return {"sources": list(SOURCES.keys())}