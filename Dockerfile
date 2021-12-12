FROM python:3.7.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements-fastapi.txt .
RUN pip install -r requirements-fastapi.txt

COPY . .

RUN mkdir -p /app/model
RUN curl -o /app/model/model.ckpt-430000.meta http://static.spanking.wiki/models/model.ckpt-430000.meta
RUN curl -o /app/model/model.ckpt-430000.index http://static.spanking.wiki/models/model.ckpt-430000.index
RUN curl -o /app/model/model.ckpt-430000.data-00000-of-00001 http://static.spanking.wiki/models/model.ckpt-430000.data-00000-of-00001
