FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    nginx \
    certbot \
    python3-certbot-nginx \
    && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 443
