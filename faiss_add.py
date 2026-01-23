import faiss
import json
import numpy as np

with open("embedding.json", "r", encoding="utf-8") as file:
    data = json.load(file)

embeddings = np.array([item["embedding"] for item in data]).astype("float32")

dimension = 1536

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print("Index içindeki toplam vektör sayısı:", index.ntotal)

faiss.write_index(index, "pdf_index.faiss")

query_vector = embeddings[0:1]
k = 3

distances, indices = index.search(query_vector, k)
print("En yakın ID'ler:", indices)
print("Uzaklıklar:", distances)