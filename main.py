from fastapi import FastAPI, status
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

    print(yeni_urun.stokta_mi)

    toplam_fiyat_kdvli = yeni_urun.fiyat * 1.2

    return {
        "mesaj": f"{yeni_urun.isim} başarıyla eklendi",
        "fiyat": toplam_fiyat_kdvli
    }


class UserCreate(BaseModel):
    username: str
    email: str
    age: int 


class UserOut(BaseModel):
    username: str
    email: str


# This one works with path parameters. So you must give the user_id in path.
# And you must define same path parameters in function signature in order to interact with it. 
# Even if you define in the query but not in path you cannot use the variable.
# Example path : /users/5?active=false

@app.get("/users/{user_id}")
def get_user(user_id: int, active: bool = True):
    if active:
        print(user_id)

    return {"status_code": status.HTTP_200_OK}

# This one works with query parameters only.
# Example path : /users?user_id=5&active=false

@app.get("/users")
def get_user(user_id: int, active: bool = True):
    if active:
        print(user_id)

    return {"status_code": status.HTTP_202_ACCEPTED}


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    return user
