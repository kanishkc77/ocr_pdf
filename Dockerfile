FROM python:3.9-slim-buster

RUN apk update && \
    apk -qq -y install tesseract-ocr && \
    apk -qq -y install libtesseract-dev \
    apk -qq -y install ghostscript

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
