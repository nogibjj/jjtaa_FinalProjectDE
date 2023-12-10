FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONFAULTHANDLER 1

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 50505

ENTRYPOINT ["gunicorn", "main:app"]
