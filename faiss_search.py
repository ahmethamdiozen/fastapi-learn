import faiss
import numpy as np
from embedding_uret import embedding_uret
import json


index = faiss.read_index("pdf_index.faiss")

with open("chunks.json", "r", encoding="utf-8") as file:
    text_data = json.load(file)["chunk"]


def ara(soru: str, k: int):
    soru_vektoru = np.array([embedding_uret(soru)]).astype("float32")

    distances, indices = index.search(soru_vektoru, k)

    return distances[0], indices[0]


query = "Girişimcilikte sistem kurmak neden önemlidir?"
query_2 = "Kedi mamasının içeriği nasıl olmalıdır?"
distances, indices = ara(query_2, 3)

print(f"Soru: {query_2}")
print("="*30)

for i in range(len(indices)):
    idx = indices[i]
    dist = distances[i]

    found_text = text_data[idx]

    print(f"\n[Eşleşme {i+1}] - Index: {idx} - Mesafe: {dist:.4f}")
    print(f"İçerik: {found_text[:150]}...") 
