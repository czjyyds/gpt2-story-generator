# app/main.py

from fastapi import FastAPI
from generation.generate import Generate

app = FastAPI(title="GPT2 Story Generator")
generation = Generate()

@app.get("/v1/gpt2/generate")
def generate(prefix: str):
    result = generation.generate(prefix)
    return {"generated": result}
