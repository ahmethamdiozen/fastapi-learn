from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Selam! İlk endpoint çalışıyor"}

@app.get("/selamla/{isim}")
def selamla(isim: str):
    return {"mesaj": f"Merhaba {isim}, FastAPI'a hoş geldin"}

@app.get("/health")
def health():
    return {"status": "ok"}

class Urun(BaseModel):
    isim: str
    fiyat: float
    stokta_mi: bool = True


@app.post("/urunler")
def urun_ekle(yeni_urun: Urun):
    toplam_fiyat_kdvli = yeni_urun.fiyat * 1.2

    return {
        "mesaj": f"{yeni_urun.isim} başarıyla eklendi",
        "fiyat": toplam_fiyat_kdvli
    }

