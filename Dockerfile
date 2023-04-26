FROM python:3.9-slim-buster

RUN sudo apt-get update && \
    sudo apt-get -qq -y install tesseract-ocr && \
    sudo apt-get -qq -y install libtesseract-dev \
    sudo apt-get -qq -y install ghostscript

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app"]
