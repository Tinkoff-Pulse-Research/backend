from fastapi import FastAPI, Response

import models
from services import detector, glossary

app = FastAPI()


@app.get("/term")
async def app_get_term_definition(response: Response, word: models.Text):
    """Returning a definition of provided term"""
    if not word.text:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}
    definition = glossary.get_term_definition(word.text)
    if definition is None:
        response.status_code = 404
        return {'status': "error", "message": "Provided term not found"}
    return {"status": "ok", "result": definition}


@app.post("/detect_slang")
async def app_detect_slang(response: Response, text: models.Text):
    """Detecting slang in provided text"""
    if not text.text:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}
    is_slang = detector.detect_slang(text.text)
    return {"status": "ok", "result": is_slang}


@app.get("/")
async def app_root():
    return {"status": "ok", "message": "pong"}
