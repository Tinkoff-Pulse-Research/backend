from fastapi import FastAPI, Response
import random

import models
from services import detector

app = FastAPI()


@app.post("/detect_slang")
async def app_detect_slang(response: Response, text: models.Text):
    if not text.text:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}
    is_slang = detector.detect_slang(text.text)
    return {"status": "ok", "result": is_slang}


@app.get("/")
async def app_root():
    return {"status": "ok", "message": "pong"}
