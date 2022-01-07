# app/main.py

from fastapi import FastAPI
from generation.generate import Generate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GPT2 Story Generator")
generation = Generate()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/v1/gpt2/generate")
def generate(prefix: str):
    result = generation.generate(prefix)
    return {"generated": result}
