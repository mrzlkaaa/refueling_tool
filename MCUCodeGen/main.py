import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from generator import *

class BurnForm(BaseModel):
    date: str
    days: list[float] | None = None

class NoBurnForm(BaseModel):
    temperature: float
    date: str
    kcs: dict | None = None
    # kc1: float | None = None
    # kc2: float | None = None
    # kc3: float | None = None
    

app = FastAPI()

@app.post('/generateNoBurn')
def mcu_file(form: NoBurnForm):
    if len(form.kcs) == 0:
        phy = NoBurn(temperature=form.temperature, date=form.date).writePHY()
        return {"msg1":phy}
    else:
        phy = NoBurn(temperature=form.temperature, date=form.date).writePHY()
        geo = NoBurn(date=form.date, kcs=form.kcs).writeGEO()
        return {"msg1":phy, "msg2": geo}
