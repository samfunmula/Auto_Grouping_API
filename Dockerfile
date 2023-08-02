FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src .

RUN rm requirements.txt

EXPOSE 8000

CMD uvicorn main:app --workers 1 --host 0.0.0.0 --port 8000 --timeout-keep-alive 30