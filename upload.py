import os
import shutil
from fastapi import FastAPI, UploadFile, HTTPException, File, status

app = FastAPI()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.post("/upload")
async def dosya_yukle(file: UploadFile = File(...)):
    
    # Dosya gönderilmiş mi?
    if file is None or file.filename == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lütfen bir dosya seçiniz."
        )
    
    if not file.filename.lower().endswith("pdf"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail= "Geçersiz dosya formatı. Sadece PDF kabul edilir."
        )
    
    # Sadece PDF kabul et.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Sadece PDF kabul edilir.")

    try:
    # Yüklenen yer + dosya adı ile path belirle
        dosya_yolu = os.path.join(UPLOAD_DIR, file.filename)
    # Stream mantığı ile diske kayıt.
        with open(dosya_yolu, "wb") as buffer:
            #file.file = file-like objecttir.
            shutil.copyfileobj(file.file, buffer)
    
    except Exception as e:
        #Beklenmedik hatada burası çalışsın. 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dosya kaydedilirken sunucu tarafında bir hata oluştu: {str(e)}"
        )

    return {
        "dosya_adi": file.filename,
        "icerik_turu": file.content_type,
        "mesaj": "Dosya başarıyla kaydedildi."
    }