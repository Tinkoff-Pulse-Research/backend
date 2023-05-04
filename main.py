from fastapi import FastAPI, Response

import models
from services import detector, glossary

app = FastAPI()


@app.post("/get_terms")
async def app_get_terms(response: Response, text: models.Text):
    """Detecting all terms and returning definitions in provided text"""
    if not text.text:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}
    terms = glossary.get_terms(text.text)
    return {"status": "ok", "terms": terms}


@app.get("/term/{word}")
async def app_get_term_definition(response: Response, word: str):
    """Returning a definition of provided term"""
    if not word:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}
    definition = glossary.get_term_definition(word)
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
    slang_confidence = detector.detect_slang(text.text)[0]
    is_slang = slang_confidence >= 0.5
    return {"status": "ok", "result": {"slang": bool(is_slang), "confidence": float(slang_confidence)}}


@app.get("/")
async def app_root():
    return {"status": "ok", "message": "pong"}
