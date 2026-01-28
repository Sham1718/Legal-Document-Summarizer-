import os
import json
import faiss
from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration

# ===============================
# PATHS
# ===============================
BASE_DIR = os.path.dirname(__file__)
CHUNK_DIR = os.path.join(BASE_DIR, "../rag/chunks")
META_DIR = os.path.join(BASE_DIR, "../rag/metadata")
INDEX_PATH = os.path.join(BASE_DIR, "../rag/faiss.index")

# ===============================
# MODELS
# ===============================
embedder = SentenceTransformer("all-MiniLM-L6-v2")

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
generator = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
generator.eval()

# ===============================
# LOAD FAISS INDEX
# ===============================
index = faiss.read_index(INDEX_PATH)

with open(os.path.join(META_DIR, "chunk_ids.json"), "r") as f:
    chunk_ids = json.load(f)

# ===============================
# CONFIG
# ===============================
TOP_K = 5
DISTANCE_THRESHOLD = 0.85
MIN_VALID_CHUNKS = 2
MAX_CONTEXT_CHARS = 1500

NON_LEGAL_KEYWORDS = [
    "modi", "rahul gandhi", "actor", "movie",
    "cricket", "politics", "biography",
    "who is", "what is your name"
]

# ===============================
# RAG QUESTION ANSWERING
# ===============================
def ask_rag(question: str):
    q_lower = question.lower()

    # ---- Guard: non-legal questions ----
    if any(word in q_lower for word in NON_LEGAL_KEYWORDS):
        return (
            "This system answers only questions related to legal documents.",
            []
        )

    # ---- Embed question ----
    q_emb = embedder.encode([question], convert_to_numpy=True)
    distances, indices = index.search(q_emb, TOP_K)

    context_chunks = []
    sources = []

    # ---- Retrieve relevant chunks ----
    for dist, idx in zip(distances[0], indices[0]):
        if dist <= DISTANCE_THRESHOLD and idx < len(chunk_ids):
            cid = chunk_ids[idx]
            chunk_path = os.path.join(CHUNK_DIR, cid + ".txt")

            if os.path.exists(chunk_path):
                with open(chunk_path, "r", encoding="utf-8") as f:
                    context_chunks.append(f.read().strip())
                    sources.append(cid)

    # ---- Enforce grounding ----
    if len(context_chunks) < MIN_VALID_CHUNKS:
        return (
            "The question cannot be answered using the provided legal documents.",
            []
        )

    # ---- Build context ----
    context = " ".join(context_chunks)
    context = context[:MAX_CONTEXT_CHARS]

    # ===============================
    # T5-CORRECT PROMPT (CRITICAL FIX)
    # ===============================
    prompt = (
        f"question: {question}\n"
        f"context: {context}\n"
        "answer:"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = generator.generate(
        inputs["input_ids"],
        max_new_tokens=120,
        do_sample=False,
        num_beams=2
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    # ---- Final safety net ----
    if not answer or answer.lower().startswith("question"):
        answer = "The answer could not be clearly determined from the document."

    return answer, sources
