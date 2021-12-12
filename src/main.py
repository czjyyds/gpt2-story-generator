# app/main.py

from fastapi import FastAPI
from generate import Generate

app = FastAPI(title="GPT2 Story Generator")

@app.get("/v1/gpt2/generate")
def generate(prefix: str):
    generated = Generate().generate(prefix)
    return {"generated": generated}
