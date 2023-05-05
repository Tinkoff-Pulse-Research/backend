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

    return {"status": "ok", "terms": glossary.get_terms(text.text)}


@app.get("/term/{word}")
async def app_get_term_definition(response: Response, word: str):
    """Returning a definition of provided term"""
    if not word:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}

    definition = glossary.get_term_definition(word)

    if definition is None:
        response.status_code = 404
        return {"status": "error", "message": "Provided term not found"}

    return {"status": "ok", "result": definition}


@app.post("/detect_slang")
async def app_detect_slang(response: Response, text: models.Text):
    """Detecting slang in provided text"""
    if not text.text:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}

    res = {
        **{
            i: glossary.get_term_definition(text.text.split()[i])
            for i in detector.detect_slang(text.text)
        },
        **glossary.get_terms(text.text),
    }

    return {"status": "ok", "result": {"slang": bool(res), "highlight": res}}


@app.get("/")
async def app_root():
    return {"status": "ok", "message": "pong"}
