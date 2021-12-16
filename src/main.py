# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generate import Generate

app = FastAPI(title="GPT2 Story Generator")

# TODO: wildcard '*' domain should not be used in production
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

generation = Generate()

@app.get("/v1/gpt2/generate")
def generate(prefix: str):
    result = generation.generate(prefix)
    return {"generated": result}
