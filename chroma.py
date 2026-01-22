import chromadb
import json

client = chromadb.PersistentClient(path="./my_db")

collection = client.get_or_create_collection(name="pdf_chunks")

with open("vector.json", "r") as f:
    vector_json=json.load(f)

with open("chunks.json", "r") as ch:
    chunks_json=json.load(ch)


collection.add(
    embeddings=vector_json,
    documents=chunks_json,
    ids=["id1"]
)

result = collection.query(query_texts=["Girişimcilik nedir?"])

print(result)
