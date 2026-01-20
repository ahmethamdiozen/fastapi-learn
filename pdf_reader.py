from fastapi import FastAPI, HTTPException, UploadFile, File
from pypdf import  PdfReader
import io
import re

app = FastAPI()

def metin_temizle(ham_metin: str) -> str:

    # Satır sonlarını tek boşluk ile değiştirdik.
    metin = ham_metin.replace("/n", " ")

    # Birden fazla boşluğu tek boşluğa çevirdik.
    # \s+ birden fazla boşluk anlamına gelir. (tab, space, newline gibi)

    metin = re.sub("\s+", " ", metin)

    #Baştaki ve sondaki boşlukları sil.

    metin = metin.strip()

    return metin



@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF file is allowed")

    try:
        content = await file.read()
        pdf_stream = io.BytesIO(content)

        reader = PdfReader(pdf_stream)

        tum_metin = ""
        sayfa_sayisi = len(reader.pages)

        for sayfa_no in range(sayfa_sayisi):
            sayfa = reader.pages[sayfa_no]
            metin = sayfa.extract_text()

            if metin:
                tum_metin += f"\n--- Sayfa {sayfa_no + 1} ---\n" + metin
        
        return {
            "dosya_adi": file.filename,
            "toplam_sayfa": sayfa_sayisi,
            "karakter_sayisi": len(tum_metin),
            "metin": tum_metin
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occured while reading PDF file: {str(e)}")
    

@app.post("extract_and_clean")
async def extract_and_clean(file: UploadFile = File(...)):
    
    content = await file.read
    pdf_stream = io.BytesIO(content)

    reader = PdfReader(pdf_stream)

    islenmis_sayfalar = []

    for page in reader.pages:
        raw_text = page.extract_text()
        if raw_text:
            cleaned_text = metin_temizle(raw_text)

            if len(cleaned_text) > 5:
                islenmis_sayfalar.append(cleaned_text)

    final_text = " ".join(islenmis_sayfalar)

    return {
            "karakter_sayisi": len(final_text),
            "temiz_metin": final_text
    }