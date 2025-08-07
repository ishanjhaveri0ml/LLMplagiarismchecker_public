from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Tuple

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_index(text_chunks: List[str]):
    embeddings = model.encode(text_chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings

def search_similar(user_chunks: List[str], web_chunks: List[str], index, top_k: int = 3) -> List[Tuple[str, List[Tuple[str, float]]]]:
    results = []
    for chunk in user_chunks:
        embedding = model.encode([chunk]).astype("float32")
        distances, indices = index.search(embedding, top_k)
        matches = [(web_chunks[i], float(distances[0][j])) for j, i in enumerate(indices[0])]
        results.append((chunk, matches))
    return results
