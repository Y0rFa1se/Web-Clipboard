# Python 3.10-slim 이미지 기반으로 설정
FROM python:3.10-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    nginx \
    certbot \
    python3-certbot-nginx \
    && rm -rf /var/lib/apt/lists/*

# Gunicorn 설치
RUN pip install gunicorn

# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/nginx.conf

# 애플리케이션 코드 복사
COPY . /app
WORKDIR /app

# 필요 패키지 설치
RUN pip install -r requirements.txt

# Nginx 및 애플리케이션 포트 노출
EXPOSE 443

# 시작 스크립트 실행 (Nginx와 애플리케이션을 동시에 실행)
CMD ["sh", "-c", "nginx && gunicorn -b 0.0.0.0:8000 app:app"]

