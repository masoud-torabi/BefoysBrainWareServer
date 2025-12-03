import pandas as pd
import numpy as np
import faiss
import pickle
from langchain_ollama import OllamaEmbeddings

index = faiss.read_index("./database_suppliers/befoys_suppliers_database.bin")
with open("./database_suppliers/befoys_suppliers_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

embeddings_model = OllamaEmbeddings(model="bge-m3:567m")

def get_ollama_embeddings(texts):
    if not isinstance(texts, list):
        texts = [texts]
    embeddings = embeddings_model.embed_documents(texts)
    return np.array(embeddings, dtype=np.float32)

def clearTextData(row: pd.Series) -> str:
    return (
        'صنف: ' + str(row['category']) + ' | ' +
        'نام و نام خانوادگی: ' + str(row['firstName']) + ' ' + str(row['lastName']) + ' | ' +
        'نام مجموعه: ' + str(row['name']) + ' | ' +
        'موبایل: 0' + str(row['mobile']) + ' | ' +
        'آدرس: ' + str(row['address'])
    )

def search_top_k_suppliers(query, k=5) -> dict:
    query_vector = get_ollama_embeddings(query)
    distances, indices = index.search(query_vector, k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        supplier = metadata[idx]
        distance = float(dist)
        results.append(clearTextData(supplier))

    output = {
        "query": query,
        "data": results
    }
    
    return output

