from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

def embedding_uret(metin: str) -> list[float]:

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=metin
    )

    return response.data[0].embedding


with open("chunks.json", "r") as file:
    chunks = json.load(file)["chunk"]


v_db_taslak = []

for text in chunks:
    print("Vektör üretiliyor:", text[:20])
    vector = embedding_uret(text)


    with open("vector.json", "w") as vector_file:
        json.dump(vector, vector_file)

    v_db_taslak.append(
        {
            "text": text,
            "embedding": vector
        }
    )

#with open("embedding.json", "w") as file:
#    json.dump(v_db_taslak, file)
