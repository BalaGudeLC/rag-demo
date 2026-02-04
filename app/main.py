import os
from fastapi import FastAPI, UploadFile, File, Query
from pypdf import PdfReader
from dotenv import load_dotenv

from app.embedding_service import get_embedding
from app.qdrant_service import init_collection, store_chunk, search_similar
from app.llm_service import answer_with_context

load_dotenv()

app = FastAPI()


def chunk_text(text: str, chunk_size=450, overlap=80):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap

    print(f"[INFO] chars={len(text)} chunks={len(chunks)} chunk_size={chunk_size} overlap={overlap}")
    return chunks


# -------------------------
# Ingest PDF
# -------------------------
@app.post("/ingest")
def ingest_pdf(file: UploadFile = File(...)):
    reader = PdfReader(file.file)

    full_text = ""
    for page in reader.pages:
        full_text += (page.extract_text() or "") + "\n"

    chunks = chunk_text(full_text)

    first_vec = get_embedding(chunks[0])
    init_collection(len(first_vec))

    for c in chunks:
        vec = get_embedding(c)
        store_chunk(c, vec)

    return {"status": "ok", "chunks": len(chunks)}


# -------------------------
# Search: retrieval only
# -------------------------
@app.post("/search")
def search(query: str = Query(..., description="User question")):
    q_emb = get_embedding(query)
    results = search_similar(q_emb, limit=3)   # default top-3
    return results


# -------------------------
# Answer: retrieval + LLM
# -------------------------
@app.post("/answer")
def answer(query: str = Query(..., description="User question")):
    # 1) embed question
    q_emb = get_embedding(query)

    # 2) retrieve top-3 chunks
    matches = search_similar(q_emb, limit=3)

    contexts = [m["text"] for m in matches]

    # 3) guardrail against hallucination
    if not contexts:
        return "I couldn’t find relevant information in the document for this question."

    # 4) LLM grounded answer
    final_answer = answer_with_context(query, contexts)

    return final_answer
