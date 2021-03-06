import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from generator import *

class BurnForm(BaseModel):
    days: list[float] | None = None
    fc_name:int

class NoBurnForm(BaseModel):
    fc_name:int
    option: str
    ar: int
    kc1: int
    kc2: int
    kc3: int
    temp: int
    



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @app.get("/login") #* AUTH to submit token
# def token(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

@app.post('/generateNoBurn')
def mcu_file(form: NoBurnForm):
    phy = NoBurn(temperature=form.temp, fc_name=form.fc_name).writePHY()
    match form.option:
        case "margin":
            return phy
        case "criticality":
            # phy = NoBurn(temperature=form.temp).writePHY()
            geo = NoBurn(kcs={
                "kc1":form.kc1, "kc2":form.kc2, "kc3":form.kc3, "ar": form.ar}).writeGEO()
            return phy, geo

@app.post('/generateBurn')
def mcu_file(form: BurnForm):
        geo = Burn(days=form.days, fc_name=form.fc_name).write()
        return geo
