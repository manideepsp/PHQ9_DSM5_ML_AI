"""
Local PDF Chat Pipeline using BGE-M3 + PyTorch + Qdrant
"""

import os
import uuid
import numpy as np
from typing import List
import fitz  # PyMuPDF
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# =============================
# PDF -> Text -> Chunks
# =============================
def pdf_to_pages(pdf_path: str) -> List[str]:
    doc = fitz.open(pdf_path)
    return [page.get_text("text") for page in doc]

def pages_to_chunks(pages: List[str], chunk_size: int = 1000, overlap: int = 100):
    chunks = []
    for page_no, text in enumerate(pages):
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append({
                "id": str(uuid.uuid4()),
                "page_no": page_no + 1,
                "chunk_index": len(chunks),
                "text": chunk
            })
            start = end - overlap
    return chunks

# =============================
# Embedding helpers
# =============================
def create_embeddings(model: SentenceTransformer, texts: List[str], batch_size: int = 32, normalize: bool = True) -> np.ndarray:
    all_embs = []
    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding batches"):
        batch = texts[i:i+batch_size]
        emb = model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
        emb = np.array(emb, dtype=np.float32)
        if normalize:
            norms = np.linalg.norm(emb, axis=1, keepdims=True)
            norms[norms==0] = 1.0
            emb = emb / norms
        all_embs.append(emb)
    return np.vstack(all_embs).astype(np.float32)

def create_embedding(model: SentenceTransformer, text: str, normalize: bool = True) -> np.ndarray:
    emb = model.encode([text], convert_to_numpy=True, show_progress_bar=False)[0]
    emb = np.array(emb, dtype=np.float32)
    if normalize:
        n = np.linalg.norm(emb)
        if n==0: n=1.0
        emb = emb / n
    return emb

# =============================
# Qdrant Index + Search
# =============================
def index_pdf(pdf_path: str, client: QdrantClient, collection_name: str, model: SentenceTransformer):
    pages = pdf_to_pages(pdf_path)
    chunks = pages_to_chunks(pages)

    texts = [c["text"] for c in chunks]
    embeddings = create_embeddings(model, texts)

    # Ensure collection exists
    vector_dim = model.get_sentence_embedding_dimension()
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE),
        )

    # Upsert
    points = []
    for ch, emb in zip(chunks, embeddings):
        payload = {"text": ch["text"], "page_no": ch["page_no"], "chunk_index": ch["chunk_index"]}
        points.append(PointStruct(id=ch["id"], vector=emb.tolist(), payload=payload))

    client.upsert(collection_name=collection_name, points=points)
    print(f"[INFO] Indexed {len(chunks)} chunks into collection '{collection_name}'.")

def search_pdf(query: str, client: QdrantClient, collection_name: str, model: SentenceTransformer, top_k: int = 5):
    q_emb = create_embedding(model, query).tolist()
    hits = client.search(collection_name=collection_name, query_vector=q_emb, limit=top_k, with_payload=True)
    return hits

# =============================
# Example Usage
# =============================
if __name__ == "__main__":
    PDF_PATH = r"C:\Users\Manideep S\OneDrive - COGNINE\POC-AI-Powered Mental Health Prediction using PHQ-9 (DSM-5)\tools\embeddings\depression-in-adults-treatment-and-management-pdf-66143832307909.pdf"  # replace with your PDF
    COLLECTION_NAME = "pdf_bge_m3"
    QDRANT_URL = os.getenv("QDRANT_URL", "https://00730b2f-77be-470e-ada2-8595e94ccaed.us-east4-0.gcp.cloud.qdrant.io")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.khYwkLnvfdbX-d4jW3sIw2o9BxYuUDICh-tdUsT-nSU")

    # Initialize model locally (CPU or GPU)
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("BAAI/bge-m3", device=device)

    # Initialize Qdrant client
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Index PDF
    index_pdf(PDF_PATH, client, COLLECTION_NAME, model)

    # Search example
    query = "Summarize the main findings"
    results = search_pdf(query, client, COLLECTION_NAME, model, top_k=3)
    for r in results:
        print(f"Score={r.score:.4f} Page={r.payload['page_no']} Text={r.payload['text'][:150]}...")
