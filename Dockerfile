FROM python:alpine

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    sqlite-dev \
    build-base \
    openssl-dev \
    python3-dev

COPY ./app .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
