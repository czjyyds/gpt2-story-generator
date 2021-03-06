# gpt2-story-generator

## Generate.py
A simple Python module that wraps and refactors the existing generation scripts from the GP2-ML repo:

https://github.com/imcaspar/gpt2-ml


## Run Locally - Using Docker
1. Install Docker/Docker Desktop https://docs.docker.com/get-docker/
2. The container will require at least 6G memory.
3. Clone this repository.
4. run `bin/start` to start the Python container, run `bin/stop` to stop the Python container. The first time you run `bin/start`, it will automatically download the model, which will take a while.

## Run Locally - Hosted
1. Clone this repository.
2. Install Python. This repo is tested with Python 3.7.9.
3. Install the required modules from `requirements.txt`, or `requirements-gpu.txt` if you have supported GPUs to use.
4. Download pretrained models https://drive.google.com/drive/folders/1-DsHiKRvPpJk3V5v-wYzovtDMXtL6Tt8
and place the model files in `model` directory.
5. (Option) If you also want to set a Fastapi endpoint to test generation, use `requirements-fastapi.txt` instead. Then run `uvicorn main:app --host 0.0.0.0 --reload` from `src` directory to start the Uvicorn server.

## Generate API Endpoint
The generation API endpoint will be hosted at http://127.0.0.1:8000/v1/gpt2/generate

A prefix argument is required. e.g. http://127.0.0.1:8000/v1/gpt2/generate?prefix=测试

You will be able to change Python code under `src` directory and test the change without needing to restart your docker container or the Uvicorn server. 
A bi-directional sync between your host and the docker container is implemented using Docker bind mount and auto reload mode from Uvicorn. 

## Run on Google Colab
https://colab.research.google.com/drive/1yRGIMiUxPEjd49U5rRWsDCBu8pb-7P8D

## Pretrained Models
The pretrained models above were trained on top of the 1.5B GPT2 pretrained Chinese model.

| Size | Language | Corpus | Vocab | Link1 | Link2 | SHA256 |
| ---- | -------- | ------ | ----- | ----- | ----- | ------ |
| 1.5B Params | Chinese  | ~30G   | CLUE ( 8021 tokens )  | [**Google Drive**](https://drive.google.com/file/d/1mT_qCQg4AWnAXTwKfsyyRWCRpgPrBJS3) | [**Baidu Pan (ffz6)**](https://pan.baidu.com/s/1yiuTHXUr2DpyBqmFYLJH6A) | e698cc97a7f5f706f84f58bb469d614e<br/>51d3c0ce5f9ab9bf77e01e3fcb41d482 |
| 1.5B Params | Chinese  | ~15G   | Bert ( 21128 tokens ) | [**Google Drive**](https://drive.google.com/file/d/1IzWpQ6I2IgfV7CldZvFJnZ9byNDZdO4n) | [**Baidu Pan (q9vr)**](https://pan.baidu.com/s/1TA_3e-u2bXg_hcx_NwVbGw) | 4a6e5124df8db7ac2bdd902e6191b807<br/>a6983a7f5d09fb10ce011f9a073b183e |
