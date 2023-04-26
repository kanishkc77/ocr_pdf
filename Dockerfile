FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -qq -y \
        tesseract-ocr \
        libtesseract-dev \
        ghostscript

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
