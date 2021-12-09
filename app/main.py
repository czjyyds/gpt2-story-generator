# app/main.py

from fastapi import FastAPI

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/v1/gpt2/generate")
def read_root():
    # TODO: add generate logic here
    return {"result": "this is the result"}