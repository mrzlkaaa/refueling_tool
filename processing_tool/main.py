import uvicorn
import redis
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from refueling import *


app = FastAPI()
redis = redis.Redis(host='irt-t.ru',
                    port=6379)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/average")
async def root(file: UploadFile):
    cont = await file.read()
    pdc = list(map(lambda x: x+"\n", cont.decode("utf-8").split("\n")))
    mp, _ = Average(pdc=pdc).average_burnup()
    redis.set(file.filename, mp.tobytes())
    #* return object with name of file and cells map to display
    return {"obj": {
                    "filename": file.filename,
                    "map":mp.tolist(),
                    },
            "status": True,
            } 



# if __name__ == "__main__":
#     uvicorn.run(app, port=8000, reload=True)