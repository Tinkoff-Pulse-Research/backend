from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def app_root():
    return {"status": "ok", "message": "pong"}
