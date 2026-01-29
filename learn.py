from fastapi import FastAPI, Depends, HTTPException


app = FastAPI()

def before():

    print("I work before than route")


@app.get("/test")
def test(x = Depends(before)):
    
    return {
        "msg": "Route worked"
    }


def check(var: int):
    allowed = False
    if var > 12:
        allowed = True

    if not allowed:
        raise HTTPException(status_code=403)
    
    else:
        return {"status_code": 200}
    
@app.get("/secret")
def secret(x = Depends(check)):



    return {
        "var": x["status_code"],
        "msg": "You are in"
    }

