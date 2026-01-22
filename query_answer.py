import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def embedding_uret(metin: str) -> list[float]:

    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=metin
    )

    return response.data[0].embedding


client = chromadb.PersistentClient("./my_db")

collection = client.get_or_create_collection("pdf_knowledge")

query  = "Fırsat Mühendisliği nedir?"

soru_vektoru = embedding_uret(query)

results = collection.query(
    query_embeddings=[soru_vektoru],
    n_results=4
)
    

print("Sonuçlar\n")

for i, doc in enumerate(results['documents'][0]):
    mesafe = results['distances'][0][i] # Benzerlik skoru (ne kadar küçükse o kadar yakın)
    print(f"\n[Kaynak Parça {i+1}] (Mesafe: {mesafe:.4f}):")
    print(f"{doc}")
    print("-" * 20)
