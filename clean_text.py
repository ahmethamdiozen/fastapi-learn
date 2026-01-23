from fastapi import FastAPI, HTTPException, UploadFile, File
import io
from pypdf import PdfReader
import re
from typing import List
import json

app = FastAPI()

def clean_text(ham_metin: str) -> str:
    metin = ham_metin.replace("\n", " ")

    metin = re.sub("\s+", " ", metin)

    metin = metin.strip()

    return metin
    
def metni_parcala(metin: str, chunk_size:int = 800, overlap: int= 100) -> List[str]:

    chunks = []
    start = 0
    # Metin bitene kadar loop
    while start < len(metin):
        
        # Chunk'ın sonunu belirledik.
        end = start + chunk_size

        if end < len(metin):
            son_bosluk = metin.rfind(" ", start, end)

            if son_bosluk != -1:
                end = son_bosluk

        chunk = metin[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start >= end:
            start = end

    return chunks


@app.post("/pdf-to-json")
async def pdf_to_json(file: UploadFile=File(...)):

    content = await file.read()
    reader = PdfReader(io.BytesIO(content))

    processed_pages = []

    for page in reader.pages:
        raw_text = page.extract_text()
        if raw_text:
            cleaned_text = clean_text(raw_text)

            if len(cleaned_text) > 5:
                processed_pages.append(cleaned_text)

    final_text = " ".join(processed_pages)

    chunks = metni_parcala(final_text)
    print("Chunks type: ", type(chunks))

    data = {
        "metadata": {
            "toplam_parca": len(chunks),
            "kaynak": file.filename
        },
        "chunk": chunks
    }

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Bu dosyanin türü", type(final_text))

    return final_text
