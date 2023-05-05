from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

import models
from services import detector, glossary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    definition, key = glossary.get_term_definition(word)

    if definition is None:
        response.status_code = 404
        return {"status": "error", "message": "Provided term not found"}

    return {"status": "ok", "result": {"definition": definition, "key": key}}


@app.post("/detect_slang")
async def app_detect_slang(response: Response, text: models.Text):
    """Detecting slang in provided text"""
    if not text.text:
        response.status_code = 400
        return {"status": "error", "message": "No text provided"}

    determined_terms = {}
    for term in glossary.get_terms(text.text):
        determined_terms.update(term)

    res = {
        **{
            str(glossary.remove_punctuation(text.text).split().index(key)) + "_determined": value
            for key, value in determined_terms.items()
            if " " not in key
        },
        **{
            f"{i}_ml": glossary.get_term_definition(text.text.split()[i])[0]
            for i in detector.detect_slang(text.text)
        },
    }

    for key, value in determined_terms.items():
        if " " not in key:
            continue
        raw_text = glossary.remove_punctuation(text.text)
        first_index = raw_text[:raw_text.index(key)].count(' ')
        res[f"{first_index}:{first_index + key.count(' ')}_determined2"] = value

    return {"status": "ok", "result": {"slang": bool(res), "highlight": res}}


@app.get("/")
async def app_root():
    return {"status": "ok", "message": "pong"}
