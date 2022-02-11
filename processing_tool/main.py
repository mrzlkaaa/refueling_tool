import uvicorn
import sys
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from refueling import *


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://109.123.162.90:80",
    "http://nss-irt-t.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

convert_to_bytes = lambda x: bytes("".join(x), "UTF-8")

class RefuelFormData(BaseModel):
    action: str
    faNums: str
    pdc: list

@app.post("/average")
async def average(file: UploadFile):
    cont = await file.read()
    pdc = list(map(lambda x: x+"\n", cont.decode("utf-8").split("\n")))
    mp, pdc = Average(pdc=pdc).average_burnup()
    #* return object with name of file and cells map to display
    return {
                "map":mp.tolist(),
                "pdc": pdc,
                "description":"initial core config",
                "status": True,
            }

@app.post("/changes")
async def changes(form: RefuelFormData):
    # pdc = list(map(lambda x: x+"\n", redis.get(form.filename).decode("utf-8").split("\n")))
    match form.action:
        case "fresh":
            mp, pdc = Fresh(form.faNums, pdc=form.pdc).refueling()
        case "swap":
            mp, pdc = Swap(form.faNums, pdc=form.pdc).swap()
    # redis.set(f"{filename}", convert_to_bytes(pdc))
    #* return object with name of file and cells map to display
    return {
                "map":mp.tolist(),
                "pdc": pdc,
                "description": "",
                "status": True,
            }
           