import faiss
import json
import os
import glob
import numpy as np
from langchain_community.embeddings import OllamaEmbeddings

index = faiss.read_index("./database/public/public_database.index")
metadata = json.load(open("./database/public/public_database_metadata.json", encoding="utf-8"))
emb = OllamaEmbeddings(model="bge-m3:567m")


def search_text_data(query, top_k=5):
    
    folder = "./database/public/files/*.txt"
    documents = []
    doc_metadata = []

    for file_path in glob.glob(folder):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        parts = [p.strip() for p in content.split("*****") if p.strip() != ""]
        filename = os.path.basename(file_path)
        for idx, part in enumerate(parts):
            documents.append(part)
            doc_metadata.append({"file": filename, "part": idx + 1})


    q_emb = np.array(emb.embed_query(query), dtype=np.float32).reshape(1, -1)
    distances, ids = index.search(q_emb, top_k)

    results = []
    for dist, idx in zip(distances[0], ids[0]):
        results.append({
            "text": documents[idx],
            "metadata": metadata[idx],
            "distance": float(dist)
        })
    return results

