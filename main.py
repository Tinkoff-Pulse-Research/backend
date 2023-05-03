from fastapi import FastAPI
import random

import models

app = FastAPI()


@app.post("/detect_slang")
async def app_detect_slang(text: models.Text):
    is_slang = random.choice([True, False])
    return {"status": "ok", "result": is_slang}


@app.get("/")
async def app_root():
    return {"status": "ok", "message": "pong"}
