from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

def embedding_uret(metin: str) -> list[float]:

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=metin
    )

    return response.data[0].embedding