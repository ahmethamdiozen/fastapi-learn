import chromadb
import json

client = chromadb.PersistentClient(path="./my_db")

collection = client.get_or_create_collection(name="pdf_knowledge")

with open("embedding.json", "r", encoding="utf-8") as file:
    v_db_draft = json.load(file)


ids = []
documents = []
embeddings = []


for i, item in enumerate(v_db_draft):
    ids.append(f"id_{i}")
    documents.append(item["text"])
    embeddings.append(item["embedding"])


collection.add(
    ids,
    documents=documents,
    embeddings=embeddings
)